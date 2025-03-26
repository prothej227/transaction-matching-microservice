from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(ar_text, bank_text, bert_model, tfidf_vectorizer):
    # TF-IDF Cosine Similarity
    tfidf_matrix = tfidf_vectorizer.fit_transform([ar_text, bank_text])
    tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # BERT Cosine Similarity
    ar_bert_embedding = bert_model.encode([ar_text])[0]
    bank_bert_embedding = bert_model.encode([bank_text])[0]
    bert_similarity = cosine_similarity([ar_bert_embedding], [bank_bert_embedding])[0][0]

    # Combined similarity with configurable weight
    combined_similarity = 0.5 * tfidf_similarity + 0.5 * bert_similarity

    return {
        "tfidf": tfidf_similarity,
        "bert": bert_similarity,
        "combined": combined_similarity
    }