import sqlalchemy as sa
from datetime import datetime, timezone
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from src.exceptions.app_exception import DatabaseException
from src.extensions import db, logger

class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class BaseModel(db.Model):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_at = sa.Column(
        sa.DateTime(), 
        default=datetime.now(timezone.utc),
        server_default=utcnow(),
        nullable=False
    )
    updated_at = sa.Column(
        sa.DateTime(),
        default=datetime.now(timezone.utc),
        server_default=utcnow(),
        onupdate=utcnow(),
        server_onupdate=utcnow(),
        nullable=False,

    )
    deleted_at = sa.Column(
        sa.DateTime(),
        default=None
    )
    is_deleted = sa.Column(sa.Boolean(), default=False, server_default="false")

    def add(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"Added to { self.__tablename__ } :: ID { self.id }")
            return None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error while adding to { self.__tablename__ } :: ID { self.id }")
            raise DatabaseException(e)

    def update(self, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.updated_at = datetime.now()
            db.session.add(self)
            db.session.commit()
            logger.info(f"Updated on { self.__tablename__ } :: ID { self.id }")
            return None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error while updating from { self.__tablename__ } :: ID { self.id }")
            raise DatabaseException(e)
        
    def delete(self) -> None:
        try:
            self.is_deleted = True
            self.deleted_at = datetime.now(timezone.utc)

            db.session.add(self)
            db.session.commit()
            logger.info(f"Deleted on { self.__tablename__ } :: ID { self.id }")
            return None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error while deleting from { self.__tablename__ } :: ID { self.id }")
            raise DatabaseException(e)
    
    def hard_delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info(f"Hard-deleted from { self.__tablename__ } :: ID { self.id }")
            return None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error while hard deleting from { self.__tablename__ } :: ID { self.id }")
            raise DatabaseException(e)

    @classmethod
    def get_all(cls):
        try:
            return cls.query.filter(cls.is_deleted.is_(False)).all()
        except Exception as e:
            logger.error(f"Error while get all from { cls.__tablename__ } :: ID { cls.id }")
            raise DatabaseException(e)
    
    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.query.filter(cls.is_deleted.is_(False), cls.id == id).first()
        except Exception as e:
            logger.error(f"Error while get by id from { cls.__tablename__ } :: ID { cls.id }")
            raise DatabaseException(e)
