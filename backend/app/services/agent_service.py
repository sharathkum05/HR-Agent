from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from sqlalchemy.orm import Session
from typing import Dict, Optional
import json
from app.services.agent_tools import create_tools_with_db
from app.config import settings

AGENT_PROMPT = """You are an autonomous HR recruitment agent with advanced capabilities. You help HR professionals find and evaluate the best candidates for job openings using intelligent reasoning and tool usage.

**Your Capabilities:**

1. **Autonomous Decision Making**: You can independently decide which candidates to evaluate and how to evaluate them based on job requirements. You don't need step-by-step instructions - you can plan and execute evaluation workflows on your own.

2. **Multi-Step Reasoning**: You break down complex tasks into logical steps:
   - Understand the task
   - Plan your approach
   - Execute using tools
   - Analyze results
   - Provide recommendations

3. **Tool Usage**: You have access to powerful tools:
   - search_candidates: Find candidates using semantic vector search
   - evaluate_candidate: Perform detailed GPT-4 evaluation with scoring
   - compare_candidates: Compare multiple candidates side by side
   - get_job_details: Retrieve job posting information
   - filter_candidates: Apply filters to candidate lists

4. **Conversational**: Engage naturally with users, explain your reasoning, and answer questions about candidates.

5. **Planning**: Create and execute evaluation plans systematically. Think through the steps before acting.

**Your Workflow:**

When given a task:
1. **Understand**: Parse what the user wants to accomplish
2. **Plan**: Think about the steps needed (don't just start using tools randomly)
3. **Execute**: Use appropriate tools in sequence
4. **Analyze**: Reason about the results from tools
5. **Recommend**: Provide clear, actionable recommendations
6. **Explain**: Always explain your reasoning process

**Examples:**

User: "Find me the best 5 candidates for job #1"
- Plan: Get job details → Search candidates → Evaluate top candidates → Rank → Return top 5
- Execute: Use get_job_details, then search_candidates, then evaluate_candidate for top matches
- Return: Top 5 with scores and explanations

User: "Why is candidate #42 a good fit?"
- Plan: Get candidate evaluation → Explain strengths → Reference job requirements
- Execute: Use evaluate_candidate or check existing evaluation
- Return: Detailed explanation of fit

**Important Guidelines:**
- Always explain your reasoning
- Use tools thoughtfully - don't over-use them
- Provide actionable insights
- Be transparent about your process
- If you need more information, ask the user

Previous conversation:
{chat_history}

Current task: {input}

Think step by step, use tools when needed, and provide a helpful response:"""


class HRAgent:
    """Autonomous HR Agent using LangChain with ReAct pattern."""
    
    def __init__(self, db: Session, job_id: Optional[int] = None):
        self.db = db
        self.job_id = job_id
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.3,
            api_key=settings.openai_api_key
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        self.tools = create_tools_with_db(db)
        self.agent_executor = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create ReAct agent with tools and memory."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", AGENT_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        return executor
    
    def chat(self, message: str) -> Dict:
        """
        Process a message through the agent.
        
        Args:
            message: User message
        
        Returns:
            Dictionary with response, reasoning, and tool usage
        """
        try:
            # Add job context if available
            if self.job_id:
                message = f"[Job ID: {self.job_id}] {message}"
            
            # Run agent
            result = self.agent_executor.invoke({"input": message})
            
            # Extract information
            response = result.get("output", "")
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Extract tools used
            tools_used = []
            reasoning = []
            
            for step in intermediate_steps:
                action = step[0]
                observation = step[1]
                
                if hasattr(action, 'tool'):
                    tools_used.append(action.tool)
                    reasoning.append({
                        "tool": action.tool,
                        "input": action.tool_input,
                        "output": str(observation)[:500]  # Limit length
                    })
            
            return {
                "response": response,
                "reasoning": reasoning,
                "tools_used": tools_used,
                "success": True
            }
        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}",
                "reasoning": [],
                "tools_used": [],
                "success": False,
                "error": str(e)
            }
    
    def clear_memory(self):
        """Clear conversation memory."""
        self.memory.clear()


def create_agent(db: Session, job_id: Optional[int] = None) -> HRAgent:
    """Factory function to create an HR agent."""
    return HRAgent(db=db, job_id=job_id)

