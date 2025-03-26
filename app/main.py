from fastapi import FastAPI, Depends, HTTPException, status
from app.schemas import MatchingRequest, MatchingResponse
from app.services import TransactionMatcher
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI(
    title="Transaction Matching Microservice",
    version="1.0.0",
    description="ML-powered microservice that performs machine learning-powered two-way matching between Open AR entries and Bank statements."
)

@app.on_event("startup")
async def load_models():
    app.state.bert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    app.state.tfidf_vectorizer = TfidfVectorizer()

def get_matcher():
    return TransactionMatcher(
        bert_model=app.state.bert_model,
        tfidf_vectorizer=app.state.tfidf_vectorizer
    )

@app.post("/match", response_model=MatchingResponse)
async def match_transactions(request: MatchingRequest, matcher: TransactionMatcher = Depends(get_matcher)):
    try: 
        result = matcher.match(request.dict())
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Server-related error occured.")
    return result