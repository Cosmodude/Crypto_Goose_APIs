import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey, Boolean,Integer,Numeric
from db.db_conf import Base


class User(Base):

    __tablename__ = 'users_pre'

    id = Column("id",Integer, primary_key=True, index=True)
    name = Column("name",String(30), nullable=False)
    email=Column("email",String(50))
    feedback=Column("feedback",Text)
    entry_time=Column("entry_time", DateTime)
    
    def __repr__(self):
        return f'{self.id}: {self.first_name}: last_name={self.last_name}'
        