key = "33b34d9607034fd9b2a58622e47dc44c"
endpoint = "https://preetiresource.cognitiveservices.azure.com/"



from flask import Flask
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from flask import Flask, render_template, request
import os

def authenticate_client():
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=ta_credential)
        return text_analytics_client
client = authenticate_client()

def sentiment_analysis_example(client, data):
    documents = data


    # Create client using endpoint and key
                
    credential = AzureKeyCredential(key)
    cog_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    
    # Get language

                
    detectedLanguage = cog_client.detect_language(documents=documents)[0]
    print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))


    # Get sentiment


    sentimentAnalysis = cog_client.analyze_sentiment(documents=documents)[0]
    print("\nSentiment: {}".format(sentimentAnalysis.sentiment))

    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
            sentimentAnalysis.confidence_scores.positive,
            sentimentAnalysis.confidence_scores.neutral,
            sentimentAnalysis.confidence_scores.negative,
            ))

                    
        # Get key phrases
        
    phrases = cog_client.extract_key_phrases(documents=documents)[0].key_phrases
    if len(phrases) > 0:
        print("\nKey Phrases:")
    for phrase in phrases:
        print('\t{}'.format(phrase))
                    
    # Get entities

    entities = cog_client.recognize_entities(documents=documents)[0].entities
    if len(entities) > 0:
        print("\nEntities")
    for entity in entities:
        print('\t{} ({})'.format(entity.text, entity.category))

    # Get linked entities

    entities = cog_client.recognize_linked_entities(documents=documents)[0].entities
    if len(entities) > 0:
            print("\nLinks")
    for linked_entity in entities:
            print('\t{} ({})'.format(linked_entity.name, linked_entity.url))


            
   #sentiment_analysis_example(client)


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
        if request.method == "POST":
            details = request.form
            global email
            email = details['email']
            sentiment_analysis_example(client, [email])
            return render_template('index.html')
        return render_template('index.html')

@app.route('/')
def score():
    return 'this is score'


if __name__ == '__main__':
        app.run()
