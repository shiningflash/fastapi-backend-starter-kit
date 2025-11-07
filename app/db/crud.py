from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD operations for SQLAlchemy models.

    Provides standard Create, Read, Update, Delete operations with type safety.
    """

    def __init__(self, *, model: Type[ModelType]) -> None:
        """
        Initialize CRUD operations for a specific model.

        Args:
            model: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: str) -> Optional[ModelType]:
        """
        Retrieve a single record by primary key.

        Args:
            db: Database session
            id: Primary key value

        Returns:
            Model instance or None if not found
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        """
        Retrieve a single record by field value.

        Args:
            db: Database session
            field: Field name to filter by
            value: Value to match

        Returns:
            Model instance or None if not found

        Raises:
            AttributeError: If field doesn't exist on model
        """
        if not hasattr(self.model, field):
            raise AttributeError(f"Model {self.model.__name__} has no field '{field}'")

        return db.query(self.model).filter(getattr(self.model, field) == value).first()

    def get_multi_by_field(
        self, db: Session, field: str, value: Any, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve multiple records by field value.

        Args:
            db: Database session
            field: Field name to filter by
            value: Value to match
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances

        Raises:
            AttributeError: If field doesn't exist on model
        """
        if not hasattr(self.model, field):
            raise AttributeError(f"Model {self.model.__name__} has no field '{field}'")

        return (
            db.query(self.model)
            .filter(getattr(self.model, field) == value)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Retrieve multiple records with pagination.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.

        Args:
            db: Database session
            obj_in: Pydantic schema with creation data

        Returns:
            Created model instance
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Update an existing record in the database.

        Args:
            db: Database session
            db_obj: Database object to update
            obj_in: Pydantic schema or dict with updated data

        Returns:
            Updated model instance
        """
        # Convert input to dictionary
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = jsonable_encoder(obj_in, exclude_unset=True)

        # Update fields that exist in input
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        # Update timestamp if model has updated_at field
        if hasattr(db_obj, "updated_at"):
            db_obj.updated_at = datetime.utcnow()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Delete a record from the database.

        Args:
            db: Database session
            id: Primary key of record to delete

        Returns:
            Deleted model instance

        Raises:
            ValueError: If record not found
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise ValueError(f"Record with id {id} not found")

        db.delete(obj)
        db.commit()
        return obj
