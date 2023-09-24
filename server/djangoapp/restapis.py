import requests
import json
from .models import CarDealer
# import related models here
from requests.auth import HTTPBasicAuth


# Function for making HTTP GET requests
def get_request(url, api_key=False, **kwargs):
    print(f"GET from {url}")
    if api_key:
        # Basic authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJraWQiOiIyMDIzMDgwOTA4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJpYW0tU2VydmljZUlkLTczZDA3YjMwLTM4NmQtNDMyOS1hOWM1LWI4NWE5ZmU0MDczNSIsImlkIjoiaWFtLVNlcnZpY2VJZC03M2QwN2IzMC0zODZkLTQzMjktYTljNS1iODVhOWZlNDA3MzUiLCJyZWFsbWlkIjoiaWFtIiwianRpIjoiNGY1NDgwNmUtZmEyOS00MzBmLThjYzEtN2QyNjZiNTA0NzVhIiwiaWRlbnRpZmllciI6IlNlcnZpY2VJZC03M2QwN2IzMC0zODZkLTQzMjktYTljNS1iODVhOWZlNDA3MzUiLCJuYW1lIjoiU2VydmljZSBjcmVkZW50aWFscy0xIiwic3ViIjoiU2VydmljZUlkLTczZDA3YjMwLTM4NmQtNDMyOS1hOWM1LWI4NWE5ZmU0MDczNSIsInN1Yl90eXBlIjoiU2VydmljZUlkIiwiYXV0aG4iOnsic3ViIjoiU2VydmljZUlkLTczZDA3YjMwLTM4NmQtNDMyOS1hOWM1LWI4NWE5ZmU0MDczNSIsImlhbV9pZCI6ImlhbS1TZXJ2aWNlSWQtNzNkMDdiMzAtMzg2ZC00MzI5LWE5YzUtYjg1YTlmZTQwNzM1Iiwic3ViX3R5cGUiOiJTZXJ2aWNlSWQiLCJuYW1lIjoiU2VydmljZSBjcmVkZW50aWFscy0xIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjA0YTY1NmNiMGVjMDQ5NDhiZGYzNDk0YjBiYzlkODZiIiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjkzNzQ2MDEwLCJleHAiOjE2OTM3NDk2MTAsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.eAzbw5gFsPIOpBpeFkLpsV-s1RDUCxkBYxsxAZ0c7PNRVwGLh0YJNO8b5PM1tGLzpaRKRgh3rtyr5KysbnX0M2giTyRel_C5P1UcwjDaeZzF1xJXGptp-tMLkXtITf8CfAo1ZnNGvK9JCFr9lGpD196esCdUjdwyHHOtlq0rBGrotKqoaGt_ttUOPUDbfnf9aVL1Atl13f6bK4fvavoTKLp_l5b15fRsh_V9F3xZVr5NnphNKV9MquI7MfQvHTefawEVgv4JBNUAgj6xfx1X6sfkf16UhavxfntM4JJIs_nyb_RE9IDztW3vXGeON0P7edDoz26ePm2tudl-jU07QA'},
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
    json_result = get_request(url, "eyJraWQiOiIyMDIzMDgwOTA4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJpYW0tU2VydmljZUlkLTczZDA3YjMwLTM4NmQtNDMyOS1hOWM1LWI4NWE5ZmU0MDczNSIsImlkIjoiaWFtLVNlcnZpY2VJZC03M2QwN2IzMC0zODZkLTQzMjktYTljNS1iODVhOWZlNDA3MzUiLCJyZWFsbWlkIjoiaWFtIiwianRpIjoiNGY1NDgwNmUtZmEyOS00MzBmLThjYzEtN2QyNjZiNTA0NzVhIiwiaWRlbnRpZmllciI6IlNlcnZpY2VJZC03M2QwN2IzMC0zODZkLTQzMjktYTljNS1iODVhOWZlNDA3MzUiLCJuYW1lIjoiU2VydmljZSBjcmVkZW50aWFscy0xIiwic3ViIjoiU2VydmljZUlkLTczZDA3YjMwLTM4NmQtNDMyOS1hOWM1LWI4NWE5ZmU0MDczNSIsInN1Yl90eXBlIjoiU2VydmljZUlkIiwiYXV0aG4iOnsic3ViIjoiU2VydmljZUlkLTczZDA3YjMwLTM4NmQtNDMyOS1hOWM1LWI4NWE5ZmU0MDczNSIsImlhbV9pZCI6ImlhbS1TZXJ2aWNlSWQtNzNkMDdiMzAtMzg2ZC00MzI5LWE5YzUtYjg1YTlmZTQwNzM1Iiwic3ViX3R5cGUiOiJTZXJ2aWNlSWQiLCJuYW1lIjoiU2VydmljZSBjcmVkZW50aWFscy0xIn0sImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjA0YTY1NmNiMGVjMDQ5NDhiZGYzNDk0YjBiYzlkODZiIiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjkzNzQ2MDEwLCJleHAiOjE2OTM3NDk2MTAsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.eAzbw5gFsPIOpBpeFkLpsV-s1RDUCxkBYxsxAZ0c7PNRVwGLh0YJNO8b5PM1tGLzpaRKRgh3rtyr5KysbnX0M2giTyRel_C5P1UcwjDaeZzF1xJXGptp-tMLkXtITf8CfAo1ZnNGvK9JCFr9lGpD196esCdUjdwyHHOtlq0rBGrotKqoaGt_ttUOPUDbfnf9aVL1Atl13f6bK4fvavoTKLp_l5b15fRsh_V9F3xZVr5NnphNKV9MquI7MfQvHTefawEVgv4JBNUAgj6xfx1X6sfkf16UhavxfntM4JJIs_nyb_RE9IDztW3vXGeON0P7edDoz26ePm2tudl-jU07QA")
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


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



