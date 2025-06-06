#Joueurs, matchs, tours (SQLAlchemy)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    pseudo = Column(String, unique=True, index=True)
    elo = Column(Integer, default=1200)
    victories = Column(Integer, default=0)
    defeats = Column(Integer, default=0)
    total_games = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    games = relationship("Game", back_populates="player1", foreign_keys='Game.player1_id')
    games_opponent = relationship("Game", back_populates="player2", foreign_keys='Game.player2_id')

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, ForeignKey("users.id"))
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    moves_count = Column(Integer, default=0)

    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])
