
# Transaction Matching Microservice

## Overview
This is a FastAPI-based microservice that performs machine learning-powered two-way matching between Open AR entries and Bank statements.

## Features
- **ML-based Matching:** Uses BERT embeddings and TF-IDF vectorization for matching.

## Installation
1. **Clone the Repository**
```
git clone <your-repo-url>
cd transaction-matching-service
```

2. **Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

## Running the Service
Start the FastAPI server by running:
```bash
uvicorn main:app --reload
```

## API Endpoints
### `/match` (POST)
- **Description:** Matches AR entries with Bank statements.
- **Request Body:**  
```json
{
    "ar_record": {
        "erpDocumentNumber": "INV123456",
        "documentDate": "2024-03-25",
        "customerNumber": "CUST001",
        "customerName": "ACME Corp",
        "paymentTerms": "Net 30",
        "dueDate": "2024-04-25",
        "invoiceAmount": 1500.0,
        "balanceAmount": 1500.0,
        "debitCreditIndicator": "D",
        "companyCode": "AC01"
    },
    "bank_statements": [
        {
            "id": 1,
            "transactionDate": "2024-03-26",
            "amount": 1500.0,
            "reference": "INV123456",
            "longText": "Payment from ACME Corp"
        },
        {
            "id": 2,
            "transactionDate": "2024-03-27",
            "amount": 1200.0,
            "reference": "INV789",
            "longText": "Partial payment"
        }
    ]
}

```
- **Response:**  
### 🚀 Example Response
```json
{
    "exact_match": [
        {
            "tfidf_similarity": 0.7092972666062738,
            "bert_similarity": 0.9373122453689575,
            "combined_similarity": 0.8233047559876157,
            "variance": 0.0,
            "variance_percentage": 0.0,
            "bank_statement_id": 1,
            "bank_reference": "INV123456",
            "bank_transaction_date": "2024-03-26",
            "bank_amount": 1500.0,
            "bank_long_text": "Payment from ACME Corp"
        }
    ],
    "possible_matches": [
        {
            "tfidf_similarity": 0.0,
            "bert_similarity": 0.6673458814620972,
            "combined_similarity": 0.3336729407310486,
            "variance": 300.0,
            "variance_percentage": 20.0,
            "bank_statement_id": 2,
            "bank_reference": "INV789",
            "bank_transaction_date": "2024-03-27",
            "bank_amount": 1200.0,
            "bank_long_text": "Partial payment"
        }
    ]
}
```

##  Future Improvements
- Add database integration to sync records between source systems  
- Add endpoints for bank statement message types ingestion (MT940, BAI2, and other SWIFT messages)  
- Add structured logging and monitoring  
## Dependencies
- FastAPI
- Sentence Transformers (BERT)
- Scikit-learn (TF-IDF Vectorizer)
- Uvicorn
