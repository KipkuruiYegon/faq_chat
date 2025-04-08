import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .models import FAQ

openai.api_key = "YOUR_OPENAI_API_KEY"


def embed_text(text):
    res = openai.embeddings.create(input=text, model="text-embedding-3-small")
    return res.data[0].embedding


def find_best_faq(user_question, top_k=1):
    user_embed = embed_text(user_question)
    faqs = FAQ.objects.exclude(embedding=None)

    faq_vectors = np.array([faq.embedding for faq in faqs])
    scores = cosine_similarity([user_embed], faq_vectors)[0]

    best_idx = scores.argsort()[::-1][:top_k]
    return faqs[best_idx[0]] if best_idx.size > 0 else None


def get_gpt_response(user_msg, faq):
    prompt = f"""
You are a helpful assistant answering based on a company FAQ.

User question: {user_msg}

Relevant FAQ:
Q: {faq.question}
A: {faq.answer}

Reply to the user using a friendly tone. If unsure, say so.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
