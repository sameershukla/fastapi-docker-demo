from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, UserBase
from app.db.db_repository import create_user, get_db, get_user, update_user, delete_user, get_all_users
import redis
import json


router = APIRouter()
redis_client = redis.StrictRedis(host='redis_db', port=6379, db=0)


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int = Path(..., title="The ID of the user to retrieve"), db: Session = Depends(get_db)):
    user_data = redis_client.get(user_id)
    if user_data is not None:
        print('returning from cache')
        return json.loads(user_data)
    else:
        db_user = get_user(db_session=db, user_id=user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user = User(**db_user.__dict__)
        redis_client.setex(user.id, 3600, json.dumps(objToDict(user)))
        return User(**db_user.__dict__)


@router.post("/users", response_model=User)
def create_new_user(user_create: UserBase, db: Session = Depends(get_db)):
    db_user, error_message = create_user(db_session=db, user_data=user_create.dict())
    if error_message:
        raise HTTPException(status_code=500, detail=error_message)
    user = User(**db_user.__dict__)
    redis_client.setex(user.id, 3600, json.dumps(objToDict(user)))
    return user


@router.put("/users/{user_id}", response_model=User)
def update_existing_user(user_update: UserBase, user_id: int = Path(..., title="The ID of the user to update"),
                         db: Session = Depends(get_db)):
    db_user = update_user(db_session=db, user_id=user_id, user_data=user_update.dict())
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user = User(**db_user.__dict__)
    redis_client.setex(user.id, 3600, json.dumps(objToDict(user)))
    return user


@router.delete("/users/{user_id}", response_model=User)
def delete_existing_user(user_id: int = Path(..., title="The ID of the user to delete"),
                         db: Session = Depends(get_db)):
    db_user = delete_user(db_session=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user =  User(**db_user.__dict__)
    redis_client.delete(user.id)
    return user


@router.get("/users", response_model=User)
def all_users(db: Session = Depends(get_db)):
    db_users = get_all_users(db_session=db)
    return [User(**{k: getattr(user, k) for k in User.__fields__}) for user in db_users]


def objToDict(user: User):
    user_dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active
    }
    return user_dict
