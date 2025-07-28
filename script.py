import boto3
import openai
import pandas as pd
import os
import io

# --- CONFIG ---
openai.api_key = os.environ['OPENAI_API_KEY']
raw_bucket_name = 'your-bucket-name'
target_bucket_name = 'target_bucket'
input_key = 'donor_interactions.csv'
output_key = 'enriched_donor_sentiment.csv'

# --- LOAD CSV FROM S3 ---
s3 = boto3.client('s3')
response = s3.get_object(Bucket=raw_bucket_name, Key=input_key)
df = pd.read_csv(io.BytesIO(response['Body'].read()))

# --- Prompt and API Call ---
def ask_openai(message):
    prompt = f"""
    Analyze this donor message. Return only this format:
    Sentiment: [positive/neutral/negative]
    Likelihood (0–100): [number]
    Theme: [theme like gratitude, concern, etc.]

    Message: "{message}"
    """
    res = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return res['choices'][0]['message']['content']

# --- Enrich Each Row ---
results = []
for _, row in df.iterrows():
    reply = row['last_text_reply']
    ai_result = ask_openai(reply)
    results.append({
        'donor_id': row['donor_id'],
        'last_donation_date': row['last_donation_date'],
        'ai_analysis': ai_result  # Raw OpenAI response
    })

# --- Save Back to S3 ---
out_df = pd.DataFrame(results)
csv_buffer = io.StringIO()
out_df.to_csv(csv_buffer, index=False)
s3.put_object(Bucket=target_bucket_name, Key=output_key, Body=csv_buffer.getvalue())
