"""Database models for the application."""

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class RequestLog(Base):
    """Model to store request metadata."""

    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    environment = Column(String(50), nullable=False)
    flask_version = Column(String(20), nullable=False)
    python_version = Column(String(100), nullable=False)
    debug_mode = Column(String(10), nullable=False)
    port = Column(String(10))
    service_name = Column(String(100))

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "environment": self.environment,
            "flask_version": self.flask_version,
            "python_version": self.python_version,
            "debug_mode": self.debug_mode,
            "port": self.port,
            "service_name": self.service_name,
        }


def get_db_session(database_url=None):
    """Create and return database session."""
    if not database_url:
        raise ValueError("Database URL must be provided")

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
