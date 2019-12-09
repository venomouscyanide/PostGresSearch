from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()
DATABASE_URI = 'postgres+psycopg2://postgres:starpark@localhost:5432/paul'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    review = Column(Text)
    tokens = Column(TSVECTOR)

    def __repr__(self):
        return "<Reviews(id='{}', review='{}', tokens={})>" \
            .format(self.id, self.review, self.tokens)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def read_csv_file(csv_file):
    row_list = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as bf:
        csvf = csv.DictReader(bf, delimiter=',', quotechar='"')
        for row in csvf:
            row_list.append(row)
    return row_list


def insert_into_reviews(list_of_reviews):
    recreate_database()
    s = Session()

    for index, review in enumerate(list_of_reviews, start=1):
        current_review = ''.join(review.sentences_list)
        reviews = Reviews(id=index, review=current_review, tokens="")
        s.add(reviews)
        s.commit()


class Review:
    def __init__(self):
        self.review_id = int()
        self.sentences_list = list()
        self.sentences_raw = list()


def tokenize():
    recreate_database()
    s = Session()
    all_reviews = s.query(Reviews).all()
    for review in all_reviews:
        current_token = func.to_tsvector('english', review.review)
        review.tokens = current_token
    s.commit()


def _lower_case_sentences(sentences_list):
    return [sentence.lower() for sentence in sentences_list]


def create_review_objects(review_file):
    with open(review_file, 'r') as review_file:
        review_counter = 0
        sentence_list = list()
        review_object = Review()
        review_object_list = list()
        for review in review_file:
            if review == '\n':
                review_object.review_id = review_counter
                review_object.sentences_raw = sentence_list
                review_object.sentences_list = _lower_case_sentences(sentence_list)
                review_object_list.append(review_object)
                sentence_list = list()
                review_counter += 1
                review_object = Review()
            else:
                sentence_list.append(review)
        review_object.review_id = review_counter
        review_object.sentences_raw = sentence_list
        review_object.sentences_list = _lower_case_sentences(sentence_list)
        review_object_list.append(review_object)
    return review_object_list


def search():
    recreate_database()
    s = Session()
    output = s.query(Reviews). \
        filter("t.token @@ to_tsquery(playstation3)"). \
        params(search_string=search_string).all()
    print(output)


def main():
    # list_of_reviews = create_review_objects("test_reviews.ft.bert.txt")
    # insert_into_reviews(list_of_reviews)
    # tokenize()
    search()


if __name__ == "__main__":
    main()
