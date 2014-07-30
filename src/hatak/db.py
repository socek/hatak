from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

DeclatativeBase = declarative_base()


def get_or_create(model, session, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        created = model(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one()


class Base(DeclatativeBase):

    @classmethod
    def get_or_create(cls, *args, **kwargs):
        return get_or_create(cls, *args, **kwargs)
