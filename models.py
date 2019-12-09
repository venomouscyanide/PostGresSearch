from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import TSVECTOR

Base = declarative_base()


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    review = Column(Text)
    tokens = Column(TSVECTOR)

    def __repr__(self):
        return "<Reviews(id='{}', review='{}', tokens={})>" \
            .format(self.id, self.review, self.tokens)
