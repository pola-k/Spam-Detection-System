from flask import Flask, request, jsonify
import joblib 
import numpy as np
import scipy.sparse as sp
import re
from spellchecker import SpellChecker
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tfidf_vectorizer = joblib.load("../tfidf_spam_classifier.pkl")
model = joblib.load("../spam_classifier.pkl")
lemmatizer = joblib.load("../spam_classifier_lemmatizer.pkl")
spell_checker = joblib.load("../spam_classifier_spell_checker.pkl")
scaler = joblib.load("../spam_classifier_scaler.pkl")
stop_words = set(stopwords.words("english"))

spam_words = spam_keywords = [
    "100% more", "100% free", "100% satisfied", "Additional income", "Be your own boss", "Best price",
    "Big bucks", "Billion", "Cash bonus", "Cents on the dollar", "Consolidate debt", "Double your cash",
    "Double your income", "Earn extra cash", "Earn money", "Eliminate bad credit", "Extra cash",
    "Extra income", "Expect to earn", "Fast cash", "Financial freedom", "Free access", "Free consultation",
    "Free gift", "Free hosting", "Free info", "Free investment", "Free membership", "Free money",
    "Free preview", "Free quote", "Free trial", "Full refund", "Get out of debt", "Get paid", "Giveaway",
    "Guaranteed", "Increase sales", "Increase traffic", "Incredible deal", "Lower rates", "Lowest price",
    "Make money", "Million dollars", "Miracle", "Money back", "Once in a lifetime", "One time",
    "Pennies a day", "Potential earnings", "Prize", "Promise", "Pure profit", "Risk-free",
    "Satisfaction guaranteed", "Save big money", "Save up to", "Special promotion", "Act now", "Apply now",
    "Become a member", "Call now", "Click below", "Click here", "Get it now", "Do it today", "Don’t delete",
    "Exclusive deal", "Get started now", "Important information regarding", "Information you requested",
    "Instant", "Limited time", "New customers only", "Order now", "Please read", "See for yourself",
    "Sign up free", "Take action", "This won’t last", "Urgent", "What are you waiting for?",
    "While supplies last", "Will not believe your eyes", "Winner", "Winning", "You are a winner",
    "You have been selected", "Bulk email", "Buy direct", "Cancel at any time", "Check or money order",
    "Congratulations", "Confidentiality", "Cures", "Dear friend", "Direct email", "Direct marketing",
    "Hidden charges", "Human growth hormone", "Internet marketing", "Lose weight", "Mass email",
    "Meet singles", "Multi-level marketing", "No catch", "No cost", "No credit check", "No fees",
    "No gimmick", "No hidden costs", "No hidden fees", "No interest", "No investment", "No obligation",
    "No purchase necessary", "No questions asked", "No strings attached", "Not junk", "Notspam",
    "Obligation", "Passwords", "Requires initial investment", "Social security number",
    "This isn’t a scam", "This isn’t junk", "This isn’t spam", "Undisclosed", "Unsecured credit",
    "Unsecured debt", "Unsolicited", "Valium", "Viagra", "Vicodin", "We hate spam", "Weight loss", "Xanax",
    "Accept credit cards", "Ad", "All new", "As seen on", "Bargain", "Beneficiary", "Billing", "Bonus",
    "Cards accepted", "Cash", "Certified", "Cheap", "Claims", "Clearance", "Compare rates",
    "Credit card offers", "Deal", "Debt", "Discount", "Fantastic", "In accordance with laws", "Income",
    "Investment", "Join millions", "Lifetime", "Loans", "Luxury", "Marketing solution",
    "Message contains", "Mortgage rates", "Name brand", "Offer", "Online marketing", "Opt in",
    "Pre-approved", "Quote", "Rates", "Refinance", "Removal", "Reserves the right", "Score",
    "Search engine", "Sent in compliance", "Subject to…", "Terms and conditions", "Trial", "Unlimited",
    "Warranty", "Web traffic", "Work from home"
]

special_chars = ["\t", "\n", "\r", "\v", "\f", "\\", "\'", "\"", "\a", "\b", "\e"]

for i in range(len(spam_words)):
    spam_words[i] = spam_words[i].lower()

def remove_special_characters(email_msg):
    email_msg = ''.join(ch if (ch not in special_chars and ch not in string.punctuation) else ' ' for ch in email_msg)
    return ' '.join(email_msg.split())

def remove_hyperlinks(email_msg):
    url_pattern = r'https?://\S+|www\.\S+|\S+\.\S+\.\S+'
    clean_text = re.sub(url_pattern, '', email_msg)
    return ' '.join(clean_text.split())

def count_spelling_mistakes(email_msg):
    words = email_msg.split()
    mistakes = spell_checker.unknown(words)
    return len(mistakes)

def count_spam_words(email_msg):
    count = sum(1 for word in spam_words if re.search(rf"\b{re.escape(word)}\b", email_msg))
    return count

def lemmatize_text(email_msg):
    if isinstance(email_msg, str):
        return " ".join([lemmatizer.lemmatize(word) for word in email_msg.split()])
    
def remove_stopwords(email_msg):
    if isinstance(email_msg, str):
        return " ".join([word for word in email_msg.split() if word not in stop_words])


@app.route("/", methods=["GET"])
def home():
    return "Spam Detection API is Running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    email = data.get("email_text")

    if not email:
        return jsonify({"error": "No email text provided"}), 400


    email = email.lower()
    URL = int(bool(re.search(r'https?://\S+|www\.\S+|\S+\.\S+\.\S+', email)))
    email = remove_special_characters(email)
    email = remove_hyperlinks(email)
    Spelling_Mistake = count_spelling_mistakes(email)
    Spam_Words = count_spam_words(email)
    email = lemmatize_text(email)
    email = remove_stopwords(email)
    scaled_values = scaler.transform(np.array([[Spam_Words, Spelling_Mistake]])) 
    Spam_Words, Spelling_Mistake = scaled_values[0]
    TFIDF = tfidf_vectorizer.transform([email])
    INPUT = sp.hstack([TFIDF, np.array([[URL, Spelling_Mistake, Spam_Words]])], format='csr')
    pred = model.predict(INPUT)

    result = "Spam" if pred[0] == 1 else "Not Spam"

    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)
