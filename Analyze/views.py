from django.http import HttpResponse
from django.shortcuts import render
key = " Your key "
endpoint = "your endpoint"



from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Returning client 
def authenticate_client():
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=ta_credential)
        return text_analytics_client

# Create your views here.
def index(request):
    print('called index')
    if request.method == 'POST':
        
        input_string = request.POST['data']
        documents = []
        result = []
        enti =[]
        entivar =[]
        linkname =[]
        linkurl =[]
        documents.append(input_string)
        # Getting azure client
        cog_client = authenticate_client()

        if ('Key' in request.POST):
                   # Get key phrases
            
            phrases = cog_client.extract_key_phrases(documents=documents)[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
            for phrase in phrases:
                phra = []
                phra.append(phrases)
                print('\t{}'.format(phrase))
                #result.append(phrases)
            return render(request,'key.html',{'keyy':phra})
            

        elif ('entity' in request.POST):
                    # Get entities

            entities = cog_client.recognize_entities(documents=documents)[0].entities
            if len(entities) > 0:

                print("\nEntities")
            for entity in entities:
                
                #enti.append(entity)
                print('\t{} ({})'.format(entity.text, entity.category))
                
                enti.append(entity.text)
                entivar.append(entity.category)

            print(enti)
            print(entivar)

            mylist = zip(enti,entivar)
            #print(mylist)

            #return render(request,'entity.html', context)

            # Get linked entities

            entities = cog_client.recognize_linked_entities(documents=documents)[0].entities
            if len(entities) > 0:
                print("\nLinks")
            for linked_entity in entities:
                #result.append(linked_entity)
                print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
                linkname.append(linked_entity.name)
                linkurl.append(linked_entity.url)
            print(linkname)
            print(linkurl)
            linklist = zip(linkname,linkurl)
            context = {
            'mylist': mylist,
            'linklist': linklist,
                      }
            
            return render(request,'entity.html',context)
    
        else:


           # Get language

            detectedLanguage = cog_client.detect_language(documents = documents)[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
            result.append(detectedLanguage.primary_language.name)

            # Get sentiment
            sentimentAnalysis = cog_client.analyze_sentiment(documents=documents)[0]
            print("\nSentiment: {}".format(sentimentAnalysis.sentiment))
            Senti = []

            Senti.append(sentimentAnalysis.sentiment)
            result.append(sentimentAnalysis.sentiment)

            print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
                sentimentAnalysis.confidence_scores.positive,
                sentimentAnalysis.confidence_scores.neutral,
                sentimentAnalysis.confidence_scores.negative,
                ))
            result.append(sentimentAnalysis.confidence_scores.positive)
            result.append(sentimentAnalysis.confidence_scores.neutral)
            result.append(sentimentAnalysis.confidence_scores.negative)




                        

        print("the results are",result)
        print(type(result))
        print(result[1])
        return render(request, 'result.html',{'result':result})
    return render(request,'index.html')
 


def result(request):
    return HttpResponse("this is result")

def keyy(request):
    return HttpResponse("this is key")

def entity(request):
    return HttpResponse("this is entities")

