# logic.py

import os
import matplotlib
# Forcefully disable Numba's caching mechanism from within the code.
# This prevents the 'no locator available' runtime error.
os.environ['NUMBA_DISABLE_CACHING'] = '1'

# Tell Matplotlib to use a non-interactive backend, suitable for servers.
matplotlib.use('Agg')
# --- END: CRITICAL FIX FOR DEPLOYMENT ---

# Now, continue with your regular imports
import torch
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import json
import time
import pandas as pd
import spacy
import collections
from collections import Counter
from typing import List, Tuple, Dict
import textstat
import io
import base64

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans, AgglomerativeClustering

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException

from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from SPARQLWrapper import SPARQLWrapper, JSON
from transformers import pipeline
# import umap
import networkx as nx
from urllib.parse import urlparse

# --- Global Variables & Initial Setup ---

# Set Hugging Face Token if available
# In a real Taipy deployment, you'd use a .env file and taipy.Config
hf_token = os.environ.get("HUGGING_FACE_HUB_TOKEN")
if hf_token:
    print("Hugging Face token set from environment variables.")
else:
    print("Hugging Face token not found. Proceeding without token.")

# Download necessary NLTK data
# DELETE OR COMMENT OUT THESE LINES
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('wordnet', quiet=True)

REQUEST_INTERVAL = 2.0
last_request_time = 0

USER_AGENTS = USER_AGENTS = [
    # --- Desktop Browsers ---
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.t (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",

    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",

    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0",

    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",

    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

    # --- Mobile Browsers ---
    # Chrome on Android
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",

    # Firefox on Android
    "Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0",

    # Safari on iPhone (iOS)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.88 Mobile/15E148 Safari/604.1", # Chrome on iOS

    # Safari on iPad (iPadOS)
    "Mozilla/5.0 (iPad; CPU OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    
    # Samsung Internet
    "Mozilla/5.0 (Linux; Android 14; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
]

# --- Model Loading ---

def load_spacy_model(model_name="en_core_web_lg"):
    """Loads a spaCy model, downloading if necessary."""
    try:
        nlp = spacy.load(model_name)
    except OSError:
        print(f"Downloading spaCy model: {model_name}...")
        spacy.cli.download(model_name)
        nlp = spacy.load(model_name)
    print("spaCy model loaded successfully.")
    return nlp

def initialize_sentence_transformer(model_name='sentence-transformers/all-MiniLM-L6-v2'):
    """Loads the Sentence Transformer model."""
    model = SentenceTransformer(model_name)
    print("Sentence Transformer model loaded successfully.")
    return model

def load_bert_ner_pipeline(model_name="dslim/bert-base-NER"):
    """Loads a BERT-based NER pipeline."""
    ner_pipeline = pipeline("ner", model=model_name, aggregation_strategy="simple")
    print("BERT NER pipeline loaded successfully.")
    return ner_pipeline

# --- Utility Functions ---

def get_random_user_agent():
    import random
    return random.choice(USER_AGENTS)

def enforce_rate_limit():
    global last_request_time
    now = time.time()
    elapsed = now - last_request_time
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)
    last_request_time = time.time()

def get_embedding(text, model):
    return model.encode(text)

def preprocess_text(text, nlp_model):
    doc = nlp_model(text)
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    return " ".join(lemmatized_tokens)

# --- Web Scraping and Content Extraction ---

def _get_selenium_driver():
    """Helper to configure and return a Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    return webdriver.Chrome(options=chrome_options)

def extract_text_from_url(url: str) -> tuple[str | None, str | None]:
    """Extracts all body text from a URL."""
    try:
        enforce_rate_limit()
        driver = _get_selenium_driver()
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, "html.parser")
        body = soup.find('body')
        if not body:
            return None, "Could not find body tag."
        for tag in body.find_all(['header', 'footer', 'nav', 'script', 'style']):
            tag.decompose()
        text = body.get_text(separator='\n', strip=True)
        return text, None
    except Exception as e:
        return None, f"Error fetching {url}: {e}"

def extract_relevant_text_from_url(url: str) -> tuple[str | None, str | None]:
    """Extracts text from main content tags (p, h, li, table)."""
    try:
        enforce_rate_limit()
        driver = _get_selenium_driver()
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, "html.parser")
        for tag in soup.find_all(["header", "footer", "nav", "script", "style"]):
            tag.decompose()
        tags = soup.find_all(["p", "ol", "ul", "h1", "h2", "h3", "h4", "h5", "h6", "table"])
        texts = [tag.get_text(separator=" ", strip=True) for tag in tags]
        return " ".join(texts), None
    except Exception as e:
        return None, f"Error extracting from {url}: {e}"
        
# --- Entity Analysis ---

def identify_entities(text: str, ner_pipeline):
    """Extracts named entities using a BERT-based NER pipeline."""
    bert_entities = ner_pipeline(text)
    entities = []
    for ent in bert_entities:
        entity_text = ent["word"].strip()
        entity_label = ent["entity_group"]
        entities.append((entity_text, entity_label))
    return entities

def count_entities(entities: List[Tuple[str, str]], nlp_model) -> Counter:
    """Counts unique (lemmatized) entities."""
    entity_counts = Counter()
    seen_entities = set()
    for entity, label in entities:
        entity = entity.replace('\n', ' ').replace('\r', '')
        if len(entity) > 2:
            doc = nlp_model(entity)
            lemma = " ".join([token.lemma_ for token in doc])
            if (lemma, label) not in seen_entities:
                entity_counts[(lemma, label)] += 1
                seen_entities.add((lemma, label))
    return entity_counts

def count_entities_total(entities: List[Tuple[str, str]], nlp_model) -> Counter:
    """Counts every occurrence of a (lemmatized) entity."""
    entity_counts = Counter()
    for entity, label in entities:
        entity = entity.replace('\n', ' ').replace('\r', '')
        if len(entity) > 2:
            doc = nlp_model(entity)
            lemma = " ".join([token.lemma_ for token in doc])
            entity_counts[(lemma, label)] += 1
    return entity_counts
    
def get_wikidata_link(entity_name: str) -> str | None:
    """Queries Wikidata for a link to the given entity."""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    safe_entity = entity_name.replace('"', '\\"')
    query = f"""
    SELECT ?item WHERE {{
      ?item rdfs:label "{safe_entity}"@en.
    }} LIMIT 1
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        bindings = results.get("results", {}).get("bindings", [])
        if bindings:
            return bindings[0]["item"]["value"]
    except Exception:
        pass
    return None
    
# --- Visualization Functions (returning objects) ---

def create_entity_barchart(entity_counts: Counter, top_n=30):
    """Creates a Plotly bar chart from entity counts."""
    if not entity_counts:
        return go.Figure()
    filtered_counts = {k: v for k, v in entity_counts.items() if k[1] != "CARDINAL"}
    df = pd.DataFrame.from_dict(filtered_counts, orient='index', columns=['count'])
    df = df.reset_index().rename(columns={'index': 'entity_info'})
    df[['entity', 'label']] = pd.DataFrame(df['entity_info'].tolist(), index=df.index)
    df = df.sort_values('count', ascending=False).head(top_n)
    
    fig = px.bar(df, x='entity', y='count', color='label',
                 title=f"Top {top_n} Most Frequent Entities",
                 labels={'entity': 'Entity', 'count': 'Frequency'},
                 hover_data=['label'])
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_wordcloud_image(entity_counts: Counter) -> str:
    """Generates a WordCloud and returns it as a base64 encoded image string."""
    if not entity_counts:
        return ""
    aggregated = {}
    for key, count in entity_counts.items():
        k = key[0] if isinstance(key, tuple) else key
        aggregated[k] = aggregated.get(k, 0) + count

    if not aggregated:
        return ""

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(aggregated)
    
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def create_entity_relationship_graph_image(entities, relationships, entity_counts) -> str:
    """Creates a NetworkX graph image and returns it as a base64 string."""
    G = nx.Graph()
    for entity, entity_type in entities:
        G.add_node(entity, type=entity_type, count=entity_counts.get(entity, 0))

    relationship_counts = Counter(relationships)
    for (e1, e2), count in relationship_counts.items():
        G.add_edge(e1, e2, weight=count)
    
    if not G.nodes:
        return ""

    plt.figure(figsize=(20, 16))
    pos = nx.spring_layout(G, seed=42, k=0.6)
    node_sizes = [G.nodes[node].get('count', 1) * 300 for node in G.nodes()]
    
    color_map = {'ORG': 'skyblue', 'GPE': 'lightgreen', 'LOC': 'lightcoral', 'WORK_OF_ART': 'plum', 'PRODUCT': 'palegoldenrod'}
    node_colors = [color_map.get(G.nodes[node].get('type'), 'lightgray') for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=[d['weight'] for _, _, d in G.edges(data=True)], alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    plt.title("Entity Relationship Graph", fontsize=16)
    plt.axis("off")
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close()
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


# --- Cosine Similarity Logic ---

def calculate_overall_similarity(urls: List[str], search_term: str, model):
    search_term_embedding = get_embedding(search_term, model)
    results = []
    errors = []
    for url in urls:
        text, err = extract_text_from_url(url)
        if text:
            text_embedding = get_embedding(text, model)
            similarity = cosine_similarity([text_embedding], [search_term_embedding])[0][0]
            results.append((url, similarity, len(text.split())))
        else:
            results.append((url, None, 0))
            if err: errors.append(err)
    return results, errors

def calculate_sentence_similarity(text: str, search_term: str, model):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return [], []
    sentence_embeddings = [get_embedding(s, model) for s in sentences]
    search_term_embedding = get_embedding(search_term, model)
    similarities = [cosine_similarity([emb], [search_term_embedding])[0][0] for emb in sentence_embeddings]
    return sentences, similarities
    
# --- Semantic Gap Analysis Logic ---

def run_semantic_gap_analysis(competitor_texts, target_text, n_value, min_df, max_df, nlp_model, sentence_model):
    """Performs TF-IDF and BERT-based gap analysis."""
    
    # Preprocess texts
    processed_competitor_texts = [preprocess_text(text, nlp_model) for text in competitor_texts]
    processed_target_text = preprocess_text(target_text, nlp_model)

    # TF-IDF
    vectorizer = TfidfVectorizer(ngram_range=(n_value, n_value), min_df=min_df, max_df=max_df, stop_words="english")
    tfidf_matrix_competitors = vectorizer.fit_transform(processed_competitor_texts)
    feature_names = vectorizer.get_feature_names_out()
    
    target_tfidf_vector = vectorizer.transform([processed_target_text])
    
    # BERT embeddings
    target_embedding = get_embedding(processed_target_text, sentence_model)
    competitor_embeddings = [get_embedding(text, sentence_model) for text in processed_competitor_texts]

    # Calculate gap scores
    gap_scores = []
    for i, comp_text in enumerate(processed_competitor_texts):
        comp_tfidf_scores = tfidf_matrix_competitors.toarray()[i]
        for j, ngram in enumerate(feature_names):
            comp_tfidf = comp_tfidf_scores[j]
            if comp_tfidf > 0:
                target_tfidf = target_tfidf_vector[0, j]
                tfidf_diff = comp_tfidf - target_tfidf
                
                if tfidf_diff > 0:
                    ngram_embedding = get_embedding(ngram, sentence_model)
                    comp_sim = cosine_similarity([ngram_embedding], [competitor_embeddings[i]])[0][0]
                    target_sim = cosine_similarity([ngram_embedding], [target_embedding])[0][0]
                    bert_diff = comp_sim - target_sim
                    
                    # Simple scoring (can be refined)
                    score = (0.4 * tfidf_diff) + (0.6 * bert_diff)
                    if score > 0:
                        gap_scores.append({'ngram': ngram, 'score': score, 'competitor_index': i})
                        
    if not gap_scores:
        return pd.DataFrame(), {}
        
    df_gap = pd.DataFrame(gap_scores).sort_values('score', ascending=False)
    
    # For word cloud
    wordcloud_freq = df_gap.groupby('ngram')['score'].sum().to_dict()
    
    return df_gap, wordcloud_freq

# --- Other Tool-Specific Logic Functions ---

def analyze_gsc_data(df_before, df_after, n_topics):
    """Processes two GSC dataframes and returns aggregated results and figures."""
    df_before.rename(columns={"Top queries": "Query"}, inplace=True)
    df_after.rename(columns={"Top queries": "Query"}, inplace=True)
    
    # Merge and calculate differences
    merged_df = pd.merge(df_before, df_after, on="Query", suffixes=("_before", "_after"), how="outer").fillna(0)
    for metric in ["Clicks", "Impressions", "Position"]:
        merged_df[f"{metric}_YOY"] = merged_df[f"{metric}_after"] - merged_df[f"{metric}_before"]
        # Avoid division by zero
        merged_df[f"{metric}_YOY_pct"] = np.where(merged_df[f"{metric}_before"] != 0, 
                                                  (merged_df[f"{metric}_YOY"] / merged_df[f"{metric}_before"]) * 100, 
                                                  np.inf) # Use inf for new keywords
    
    # LDA Topic Modeling
    queries = merged_df["Query"].astype(str).tolist()
    vectorizer = CountVectorizer(stop_words="english", max_df=0.9, min_df=2)
    query_matrix = vectorizer.fit_transform(queries)
    
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    topic_dist = lda.fit_transform(query_matrix)
    
    merged_df["Topic_Num"] = topic_dist.argmax(axis=1)

    # Generate descriptive topic labels
    stop_words = set(stopwords.words('english'))
    def generate_label(queries_in_topic):
        words = " ".join(queries_in_topic).lower().split()
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        if not filtered: return "Misc Topic"
        return ", ".join([w for w, c in Counter(filtered).most_common(2)])

    topic_labels = {}
    for i in range(n_topics):
        topic_queries = merged_df[merged_df["Topic_Num"] == i]["Query"].tolist()
        topic_labels[i] = generate_label(topic_queries)
        
    merged_df["Topic"] = merged_df["Topic_Num"].map(topic_labels)
    
    # Aggregation
    agg_metrics = {f"{m}_{s}": "sum" for m in ["Clicks", "Impressions"] for s in ["before", "after", "YOY"]}
    agg_metrics.update({f"Position_{s}": "mean" for s in ["before", "after", "YOY"]})
    
    agg_df = merged_df.groupby("Topic").agg(agg_metrics).reset_index()

    # Create visualization
    vis_data = []
    for _, row in agg_df.iterrows():
        for metric in ["Clicks", "Impressions", "Position"]:
            yoy_before = row.get(f"{metric}_before", 0)
            if yoy_before != 0:
                 yoy_pct = (row.get(f"{metric}_YOY", 0) / yoy_before) * 100
                 vis_data.append({"Topic": row["Topic"], "Metric": metric, "YOY % Change": yoy_pct})
    
    vis_df = pd.DataFrame(vis_data)
    fig = px.bar(vis_df, x="Topic", y="YOY % Change", color="Metric", 
                 barmode="group", title="YOY % Change by Topic")
                 
    return merged_df, agg_df, fig

