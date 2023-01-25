import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey, Boolean,Integer,Numeric
from db.db_conf import Base


class Projects(Base):

    __tablename__ = 'nft_pr'
    __table_args__ = {'extend_existing': True}

    id = Column("id",Integer, primary_key=True, index=True)
    name = Column("project_name",String(30), nullable=False) #name of the project
    project_image_url= Column("project_image_url",String(100))
    required_token_name=Column("required_token_name",String(5) )
    chain_name=Column("chain_name",String(30))
    nft_floor_price=Column("nft_floor_price",Numeric(10,6) )
    earn_token_name=Column("earn_token_name",String(5))
    last_updated=Column("last_updated",DateTime)
    daily_earn_rate_ET=Column("earn_rate_ET",Numeric(10,6))
    nft_required=Column("nft_required",Integer)

    def __repr__(self):
        return f'{self.id}: {self.name}: floor price={self.floor_price}'
        

class Project(Base):

    __tablename__ = 'nft_pr'
    __table_args__ = {'extend_existing': True}

    id = Column("id",Integer, primary_key=True, index=True)
    name = Column("project_name",String(30), nullable=False)
    description=Column("project_description",String(1000))
    chain_name=Column("chain_name",String(30))
    earn_token_name=Column("earn_token_name",String(5))
    earn_token_image=Column("earn_token_image",String(500))
    last_updated=Column("last_updated",DateTime)
    twitter=Column("twitter_url",String(200))
    telegram=Column("telegram_url",String(200))
    webpage=Column("project_webpage_url",String(200))
    discord=Column("discord_url",String(200))
    project_image=Column("project_image_url",String(500))
    nft_floor_price=Column("nft_floor_price",Numeric(10,6) )
    daily_earn_rate_ET=Column("daily_earn_rate_ET",Numeric(10,6))
    category=Column("project_category",String(100))
    nft_required=Column("nft_required",Integer)
    nft_picture_url=Column("nft_picture_url",String(500))
    required_token_name=Column("required_token_name",String(5) )
    click_and_buy_url=Column("click_and_buy_url",String(200))
    click_to_earn_url=Column("click_to_earn_url",String(200))

    def __repr__(self):
        return f'{self.id}: {self.name}: floor price={self.site}'
        