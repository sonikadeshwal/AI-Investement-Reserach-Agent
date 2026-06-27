from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from research import graph
from ResearchAgent.research import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanyRequest(BaseModel):
    company_name: str


@app.post("/analyze")
async def analyze_company(data: CompanyRequest):

    result = graph.invoke(
        {"query": data.company_name}
    )

    return {
        "facts": result["facts"],
        "score": result["score"],
        "report": result["final_response"]
    }