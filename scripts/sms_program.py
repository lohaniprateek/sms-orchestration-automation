import requests
import json
import logging
from rate_limiter import RateLimiter
import os

# Load configuration from environment variables
COUNTRY = os.getenv("COUNTRY")
OPERATOR = os.getenv("OPERATOR")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
PROXY_DETAILS = os.getenv("PROXY_DETAILS")
SMS_GATEWAY_URL = os.getenv("SMS_GATEWAY_URL")
SMS_LIMIT_PER_MINUTE = int(os.getenv("SMS_LIMIT_PER_MINUTE", 10))

# Configure logging
logging.basicConfig(filename='logs/sms_log.log', level=logging.INFO)

# Initialize the rate limiter
rate_limiter = RateLimiter(limit=SMS_LIMIT_PER_MINUTE, interval=60)

def send_sms(phone_number, proxy):
    headers = {"Content-Type": "application/json"}
    data = {
        "phone_number": phone_number,
        "country": COUNTRY,
        "operator": OPERATOR,
        "proxy": proxy
    }
    try:
        response = requests.post(SMS_GATEWAY_URL, json=data, headers=headers, timeout=5)
        if response.status_code == 200:
            logging.info(f"SMS sent successfully to {phone_number} at {time.time()}")
            return True
        else:
            logging.error(f"Failed to send SMS to {phone_number}. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Exception occurred while sending SMS to {phone_number}: {e}")
        return False

def main():
    # Send SMS in a rate-limited way
    if rate_limiter.allow_send():
        if send_sms(PHONE_NUMBER, PROXY_DETAILS):
            print(f"Sent SMS to {PHONE_NUMBER} via {OPERATOR} in {COUNTRY}")
        else:
            print(f"Failed to send SMS to {PHONE_NUMBER}")
    else:
        print("Rate limit reached, waiting to send SMS...")
        rate_limiter.wait_until_allowed()

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)  # Slight delay to avoid spamming the API in a loop