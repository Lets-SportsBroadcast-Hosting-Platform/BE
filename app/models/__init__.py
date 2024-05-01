<<<<<<< HEAD
from sqlalchemy import Column,TEXT,INT,BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

=======
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase): pass
>>>>>>> 225624dc07f5e2c506438cd54e0b50fc1062df98
