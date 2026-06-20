import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.schemas.agent_run import AgentRunCreate, AgentRunResponse

# 1. Import your database model and backend orchestrator agent
from src.models.database_models import AgentRun
from src.agents.orchestrator import AgentOrchestrator

router = APIRouter()

@router.post("/run", response_model=AgentRunResponse, status_code=status.HTTP_201_CREATED)
async def trigger_agent_execution(
    payload: AgentRunCreate, 
    background_tasks: BackgroundTasks, # Add background task manager
    db: Session = Depends(get_db)
):
    new_run_id = str(uuid.uuid4())
    
    # 2. CREATE A REAL ROW IN YOUR SQLITE DATABASE
    db_run = AgentRun(
        id=new_run_id,
        user_query=payload.user_query,
        target_depth=payload.target_depth,
        status="queued",
        scraped_urls_json="[]",
        final_report=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    
    # 3. TRIGGER THE MULTI-AGENT WORKFLOW IN A BACKGROUND THREAD
    background_tasks.add_task(AgentOrchestrator.execute_workflow, new_run_id)
    
    return db_run

@router.get("/run/{run_id}", response_model=AgentRunResponse)
async def get_agent_status_by_id(run_id: str, db: Session = Depends(get_db)):
    # 4. LOOK UP THE REAL DATA FROM SQLITE INSTEAD OF RETURNING HARDCODED TEXT
    db_run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
    
    if not db_run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The requested research run task signature was not found on disk."
        )
        
    return db_run