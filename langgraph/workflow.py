"""
LangGraph workflow configuration for multi-agent research orchestration
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
import asyncio
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.checkpoint import PostgresSaver
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from app.core.config import settings
from app.models.job import JobStatus
from app.services.job_service import JobService
from app.services.retrieval_service import RetrievalService
from app.services.synthesis_service import SynthesisService
from app.services.drafting_service import DraftingService
from app.services.fact_checking_service import FactCheckingService
from app.services.visualization_service import VisualizationService
from app.services.export_service import ExportService


class ResearchState:
    """State object for the research workflow"""
    
    def __init__(self, job_id: UUID, query: str, constraints: Dict = None, output_config: Dict = None):
        self.job_id = job_id
        self.query = query
        self.constraints = constraints or {}
        self.output_config = output_config or {}
        self.messages: List[BaseMessage] = []
        self.sources: List[Dict] = []
        self.claims: List[Dict] = []
        self.citations: List[Dict] = []
        self.artifacts: List[Dict] = []
        self.current_node: str = "start"
        self.errors: List[str] = []
        self.metadata: Dict[str, Any] = {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            "job_id": str(self.job_id),
            "query": self.query,
            "constraints": self.constraints,
            "output_config": self.output_config,
            "messages": [msg.dict() for msg in self.messages],
            "sources": self.sources,
            "claims": self.claims,
            "citations": self.citations,
            "artifacts": self.artifacts,
            "current_node": self.current_node,
            "errors": self.errors,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResearchState":
        """Create state from dictionary"""
        state = cls(
            job_id=UUID(data["job_id"]),
            query=data["query"],
            constraints=data.get("constraints", {}),
            output_config=data.get("output_config", {})
        )
        state.messages = [BaseMessage.parse_obj(msg) for msg in data.get("messages", [])]
        state.sources = data.get("sources", [])
        state.claims = data.get("claims", [])
        state.citations = data.get("citations", [])
        state.artifacts = data.get("artifacts", [])
        state.current_node = data.get("current_node", "start")
        state.errors = data.get("errors", [])
        state.metadata = data.get("metadata", {})
        return state


class ResearchWorkflow:
    """Main research workflow orchestrator"""
    
    def __init__(self):
        self.llm_openai = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=settings.OPENAI_API_KEY
        )
        self.llm_claude = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=0.1,
            api_key=settings.ANTHROPIC_API_KEY
        )
        
        # Initialize services
        self.job_service = JobService()
        self.retrieval_service = RetrievalService()
        self.synthesis_service = SynthesisService()
        self.drafting_service = DraftingService()
        self.fact_checking_service = FactCheckingService()
        self.visualization_service = VisualizationService()
        self.export_service = ExportService()
        
        # Create workflow graph
        self.graph = self._create_workflow_graph()
    
    def _create_workflow_graph(self) -> StateGraph:
        """Create the LangGraph workflow"""
        
        # Create state graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("query_understanding", self._query_understanding_node)
        workflow.add_node("retrieval_hub", self._retrieval_hub_node)
        workflow.add_node("evidence_synthesis", self._evidence_synthesis_node)
        workflow.add_node("drafting", self._drafting_node)
        workflow.add_node("fact_checking", self._fact_checking_node)
        workflow.add_node("visualization", self._visualization_node)
        workflow.add_node("review_gate", self._review_gate_node)
        workflow.add_node("formatting", self._formatting_node)
        workflow.add_node("human_approval", self._human_approval_node)
        
        # Define edges
        workflow.set_entry_point("query_understanding")
        
        workflow.add_edge("query_understanding", "retrieval_hub")
        workflow.add_edge("retrieval_hub", "evidence_synthesis")
        workflow.add_edge("evidence_synthesis", "drafting")
        workflow.add_edge("drafting", "fact_checking")
        workflow.add_edge("fact_checking", "visualization")
        workflow.add_edge("visualization", "review_gate")
        
        # Conditional edges for review gate
        workflow.add_conditional_edges(
            "review_gate",
            self._review_gate_condition,
            {
                "approve": "formatting",
                "request_changes": "drafting",
                "human_review": "human_approval"
            }
        )
        
        workflow.add_edge("human_approval", "drafting")
        workflow.add_edge("formatting", END)
        
        # Add error handling
        workflow.add_edge("error", END)
        
        return workflow.compile(checkpointer=PostgresSaver(
            db_url=settings.DATABASE_URL,
            table_name="graph_checkpoints"
        ))
    
    async def _query_understanding_node(self, state: ResearchState) -> ResearchState:
        """Query understanding and planning node"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.PLANNING)
            
            # Expand user query and create research plan
            plan = await self._create_research_plan(state.query, state.constraints)
            
            state.metadata["research_plan"] = plan
            state.current_node = "query_understanding"
            
            # Add to messages
            state.messages.append(HumanMessage(content=state.query))
            state.messages.append(AIMessage(content=f"Research plan created: {plan['summary']}"))
            
            return state
            
        except Exception as e:
            state.errors.append(f"Query understanding failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _retrieval_hub_node(self, state: ResearchState) -> ResearchState:
        """Information retrieval node"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.RETRIEVING)
            
            # Retrieve information from multiple sources
            sources = await self.retrieval_service.retrieve_sources(
                query=state.query,
                plan=state.metadata.get("research_plan"),
                constraints=state.constraints
            )
            
            state.sources = sources
            state.current_node = "retrieval_hub"
            
            return state
            
        except Exception as e:
            state.errors.append(f"Retrieval failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _evidence_synthesis_node(self, state: ResearchState) -> ResearchState:
        """Evidence synthesis and analysis node"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.SYNTHESIZING)
            
            # Synthesize evidence from sources
            claims = await self.synthesis_service.synthesize_evidence(
                sources=state.sources,
                query=state.query
            )
            
            state.claims = claims
            state.current_node = "evidence_synthesis"
            
            return state
            
        except Exception as e:
            state.errors.append(f"Evidence synthesis failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _drafting_node(self, state: ResearchState) -> ResearchState:
        """Report drafting node"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.DRAFTING)
            
            # Generate report draft
            draft = await self.drafting_service.create_draft(
                claims=state.claims,
                sources=state.sources,
                output_config=state.output_config
            )
            
            state.metadata["draft"] = draft
            state.current_node = "drafting"
            
            return state
            
        except Exception as e:
            state.errors.append(f"Drafting failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _fact_checking_node(self, state: ResearchState) -> ResearchState:
        """Fact checking and citation verification node"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.FACT_CHECKING)
            
            # Verify claims and create citations
            verified_claims, citations = await self.fact_checking_service.verify_claims(
                claims=state.claims,
                sources=state.sources
            )
            
            state.claims = verified_claims
            state.citations = citations
            state.current_node = "fact_checking"
            
            return state
            
        except Exception as e:
            state.errors.append(f"Fact checking failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _visualization_node(self, state: ResearchState) -> ResearchState:
        """Data visualization node"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.VISUALIZING)
            
            # Create visualizations
            visualizations = await self.visualization_service.create_visualizations(
                claims=state.claims,
                sources=state.sources
            )
            
            state.artifacts.extend(visualizations)
            state.current_node = "visualization"
            
            return state
            
        except Exception as e:
            state.errors.append(f"Visualization failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _review_gate_node(self, state: ResearchState) -> ResearchState:
        """Review gate for quality control"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.REVIEWING)
            
            # Quality check
            quality_score = await self._quality_check(state)
            
            if quality_score >= 0.8:
                return "approve"
            elif quality_score >= 0.6:
                return "request_changes"
            else:
                return "human_review"
                
        except Exception as e:
            state.errors.append(f"Review gate failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _human_approval_node(self, state: ResearchState) -> ResearchState:
        """Human-in-the-loop approval node"""
        try:
            # Wait for human approval
            approval = await self._wait_for_human_approval(state.job_id)
            
            if approval == "approve":
                return "approve"
            else:
                return "request_changes"
                
        except Exception as e:
            state.errors.append(f"Human approval failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _formatting_node(self, state: ResearchState) -> ResearchState:
        """Final formatting and export node"""
        try:
            await self.job_service.update_job_status(state.job_id, JobStatus.FORMATTING)
            
            # Generate final report
            report = await self.export_service.generate_report(
                draft=state.metadata.get("draft"),
                claims=state.claims,
                citations=state.citations,
                artifacts=state.artifacts,
                output_config=state.output_config
            )
            
            state.artifacts.append(report)
            state.current_node = "formatting"
            
            # Mark job as completed
            await self.job_service.update_job_status(state.job_id, JobStatus.COMPLETED)
            
            return state
            
        except Exception as e:
            state.errors.append(f"Formatting failed: {str(e)}")
            state.current_node = "error"
            return state
    
    async def _review_gate_condition(self, state: ResearchState) -> str:
        """Condition for review gate routing"""
        return state.current_node
    
    async def _create_research_plan(self, query: str, constraints: Dict) -> Dict:
        """Create research plan from query"""
        # Implementation for research planning
        return {
            "summary": f"Research plan for: {query}",
            "sub_questions": [],
            "sources": [],
            "timeline": "2-3 hours"
        }
    
    async def _quality_check(self, state: ResearchState) -> float:
        """Perform quality check on the research"""
        # Implementation for quality checking
        return 0.85
    
    async def _wait_for_human_approval(self, job_id: UUID) -> str:
        """Wait for human approval"""
        # Implementation for human approval
        return "approve"
    
    async def start_workflow(self, job_id: UUID, query: str, constraints: Dict = None, output_config: Dict = None) -> str:
        """Start the research workflow"""
        state = ResearchState(job_id, query, constraints, output_config)
        
        # Run the workflow
        result = await self.graph.ainvoke(state)
        
        return result.current_node
