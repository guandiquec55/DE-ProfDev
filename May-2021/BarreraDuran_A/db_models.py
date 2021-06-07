
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, MetaData, DateTime, NCHAR, DECIMAL

# https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html#explicit-schema-name-with-declarative-table

metadata = MetaData(schema="Sales")

Base = declarative_base(metadata=metadata)


class CurrencyRate(Base):
    """
    The ORM definition of the table we will be interacting with in the DB (CurrencyRate)
    This enables bulk insert
    """
    __tablename__ = 'CurrencyRate'

    CurrencyRateID = Column(Integer, primary_key=True)
    CurrencyRateDate = Column(DateTime)
    FromCurrencyCode = Column(NCHAR(3))
    ToCurrencyCode = Column(NCHAR(3))
    AverageRate = Column(DECIMAL)
    EndOfDayRate = Column(DECIMAL)
    ModifiedDate = Column(DateTime)
