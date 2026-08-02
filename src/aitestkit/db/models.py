import uuid
import time
from sqlalchemy import Column, String, Float, Integer, Boolean, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class EvaluationRunDB(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String(64), primary_key=True, default=lambda: f"eval_{uuid.uuid4().hex[:8]}")
    tenant_id = Column(String(64), nullable=False)
    model_name = Column(String(64), nullable=False)
    accuracy_score = Column(Float, default=0.0)
    hallucination_score = Column(Float, default=0.0)
    is_safe = Column(Boolean, default=True)
    total_tokens = Column(Integer, default=0)
    cost_per_request = Column(Float, default=0.0)
    created_at = Column(Float, default=time.time)

# Local SQLite Engine for SaaS Persistence (Upgrade-ready for PostgreSQL)
DATABASE_URL = "sqlite:///./aitestkit_saas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)