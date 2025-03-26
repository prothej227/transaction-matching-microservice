from pydantic import BaseModel
from typing import List, Optional
from . import models

class MatchingRequest(BaseModel):
    ar_record: models.ARRecord
    bank_statements: List[models.BankStatementRecord]

class MatchResult(BaseModel):
    tfidf_similarity: float
    bert_similarity: float
    combined_similarity: float
    variance: Optional[float] = None
    variance_percentage: Optional[float] = None
    bank_statement_id: int
    bank_reference: str
    bank_transaction_date: str
    bank_amount: float
    bank_long_text: str

class MatchingResponse(BaseModel):
    exact_match: List[MatchResult]
    possible_matches: List[MatchResult]