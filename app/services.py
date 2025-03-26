import pandas as pd
from typing import Dict
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils import calculate_similarity

class TransactionMatcher:
    def __init__(self, bert_model: SentenceTransformer, tfidf_vectorizer: TfidfVectorizer):
        self.bert_model = bert_model
        self.tfidf_vectorizer= tfidf_vectorizer

    def match(self, request: Dict):
        ar_record = request['ar_record']
        bank_statements_df = pd.DataFrame(request['bank_statements'])

        if bank_statements_df.empty:
            raise ValueError("Bank statements data is empty")

        ar_text = f"{ar_record['customerName']} {ar_record['erpDocumentNumber']} {ar_record['invoiceAmount']}"

        potential_matches = []
        with_variance_possible_matches = []

        for _, bank_row in bank_statements_df.iterrows():
            bank_text = f"{bank_row['longText']} {bank_row['amount']} {bank_row['reference']}"

            similarities = calculate_similarity(
                ar_text, 
                bank_text, 
                self.bert_model, 
                self.tfidf_vectorizer
            )

            bank_amount = bank_row['amount']
            variance = ar_record['invoiceAmount'] - bank_amount
            variance_percentage = round(abs(variance) * 100 / ar_record['invoiceAmount'], 2) if bank_amount else None

            match_result = {
                "tfidf_similarity": similarities["tfidf"],
                "bert_similarity": similarities["bert"],
                "combined_similarity": similarities["combined"],
                "variance": variance,
                "variance_percentage": variance_percentage,
                "bank_statement_id": bank_row['id'],
                "bank_reference": bank_row['reference'],
                "bank_transaction_date": bank_row['transactionDate'],
                "bank_amount": bank_amount,
                "bank_long_text": bank_row['longText']
            }

            if variance == 0:
                potential_matches.append(match_result)
            else:
                with_variance_possible_matches.append(match_result)

        return {
            "exact_match": sorted(potential_matches, key=lambda x: x["combined_similarity"], reverse=True),
            "possible_matches": sorted(with_variance_possible_matches, key=lambda x: x["combined_similarity"], reverse=True)
        }
