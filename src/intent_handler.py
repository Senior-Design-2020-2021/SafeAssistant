import json
import nltk
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(nltk.corpus.stopwords.words('english'))  
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
stemmer = nltk.PorterStemmer()
SIMILARITY_CUTTOFF = 0.1

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def parse_request(inputString):
    inputTokens = nltk.tokenize.word_tokenize(inputString)  
    filteredInput = [w for w in inputTokens if not w in stop_words]  
    filteredInput = [stemmer.stem(w) for w in filteredInput]

    with open('tmp/appIndex.json') as f:
        applications = json.load(f)

    for app in applications:
        triggers = ' '.join(app["triggers"])
        triggersTokens = nltk.tokenize.word_tokenize(triggers)
        filteredTriggers =  [w for w in triggersTokens if not w in stop_words] 
        filteredTriggers = [stemmer.stem(w) for w in filteredTriggers]
        app["jaccard"] = jaccard_similarity(filteredTriggers,filteredInput)

    currentIndex = 0

    highestJaccard = 0
    highestJaccardIndex = 0

    for app in applications:
        if app["jaccard"] > highestJaccard:
            highestJaccard = app["jaccard"]
            highestJaccardIndex = currentIndex
        currentIndex += 1



    if highestJaccard <= SIMILARITY_CUTTOFF:
        return None
    else:
        requestedApp = applications[highestJaccardIndex]["name"]
        return requestedApp

