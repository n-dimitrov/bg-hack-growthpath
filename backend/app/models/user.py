from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR_ADMIN = "hr_admin"
    LEADERSHIP = "leadership"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
