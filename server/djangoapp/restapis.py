from decouple import config
import os
import requests
import json
from .models import CarDealer, DealerReview
# import related models here
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Function for making HTTP GET requests
def get_request(url, api_key=False, **kwargs):
    print(f"GET from {url}")
    iAmApiKey = 'mDsFamWdqwjivRebkJavKJZnVx5qtnADXR9grdrMH_id'
    if api_key:
        # Basic authentication GET
        try:
            headersToken = {"Content-Type": "application/x-www-form-urlencoded"}
            tokenResponse = requests.post('https://iam.cloud.ibm.com/identity/token',  headers=headersToken, data={ "grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": iAmApiKey})
            tokenRes = tokenResponse.json()
            response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer '+tokenRes.get("access_token")+''},
                                    params=kwargs)
        except:
            print("An error occurred while making GET request. ")
    else:
        # No authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            print("An error occurred while making GET request. ")

    # Retrieving the response status code and content
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)

    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url):
    results = []
    json_result = get_request(url, api_key=True)
    # Retrieve the dealer data from the response
    dealers = json_result["rows"]
    # For each dealer in the response
    for dealer in dealers:
        # Get its data in `doc` object
        dealer_doc = dealer["doc"]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
        results.append(dealer_obj)

    return results

def get_dealers_from_cf_by_id(url, dealer_id):
    dealer_obj = {}
    json_result = get_request(url, api_key=True)
    # Retrieve the dealer data from the response
    dealers = json_result["rows"]
    # For each dealer in the response
    for dealer in dealers:
        # Get its data in `doc` object
        dealer_doc = dealer["doc"]
        if(dealer_doc["id"] != dealer_id):
            continue
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])

    return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


# Gets all dealer reviews for a specified dealer from the Cloudant DB
# Uses the Cloud Function get_reviews
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Perform a GET request with the specified dealer id
    json_result = get_request(url, api_key=True)

    if json_result:
        # Get all review data from the response
        reviews = json_result["rows"]
        # For every review in the response
        for review in reviews:
            doc = review["doc"]
            # Create a DealerReview object from the data
            # These values must be present
            if(doc["dealership"] != dealer_id):
                continue
            review_content = doc["review"]
            id = doc["_id"]
            name = doc["name"]
            purchase = doc["purchase"]
            dealership = doc["dealership"]

            try:
                # These values may be missing
                car_make = doc["car_make"]
                car_model = doc["car_model"]
                car_year = doc["car_year"]
                purchase_date = doc["purchase_date"]

                # Creating a review object
                review_obj = DealerReview(dealership=dealership, id=id, name=name, 
                                          purchase=purchase, review=review_content, car_make=car_make, 
                                          car_model=car_model, car_year=car_year, purchase_date=purchase_date
                                          )

            except KeyError:
                print("Something is missing from this review. Using default values.")
                # Creating a review object with some default values
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase, review=review_content)

            # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(f"sentiment: {review_obj.sentiment}")

            # Saving the review object to the list of results
            results.append(review_obj)

    return results


# Calls the Watson NLU API and analyses the sentiment of a review
def analyze_review_sentiments(review_text):
    # Watson NLU configuration
    try:
        if os.environ['env_type'] == 'PRODUCTION':
            url = os.environ['WATSON_NLU_URL']
            api_key = os.environ["WATSON_NLU_API_KEY"]
    except KeyError:
        url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/c6e2ede9-a0b9-418e-9fa5-bc7fc70d1604"
        api_key = "rNkcvHe09DQnxvNoQpAL969ftCWdhNj3smrUIucbv8aL"

    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version=version, authenticator=authenticator)
    nlu.set_service_url(url)

    # get sentiment of the review
    try:
        response = nlu.analyze(text=review_text, features=Features(
            sentiment=SentimentOptions())).get_result()
        print(json.dumps(response))
        # sentiment_score = str(response["sentiment"]["document"]["score"])
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
        sentiment_label = "neutral"

    # print(sentiment_score)
    print(sentiment_label)

    return sentiment_label

def get_dealer_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    dealer = get_dealers_from_cf_by_id(url, dealer_id)
    return dealer
