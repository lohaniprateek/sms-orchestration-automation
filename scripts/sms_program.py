import requests
import logging
import os
import time
from prometheus_client import start_http_server, Counter
from rate_limiter import RateLimiter

# Load configuration from environment variables
COUNTRY = os.getenv("COUNTRY")
OPERATOR = os.getenv("OPERATOR")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
PROXY_DETAILS = os.getenv("PROXY_DETAILS")
SMS_GATEWAY_URL = os.getenv("SMS_GATEWAY_URL")
SMS_LIMIT_PER_MINUTE = int(os.getenv("SMS_LIMIT_PER_MINUTE", 10))

# Configure logging
logging.basicConfig(filename='logs/sms_log.log', level=logging.INFO)

# Initialize the rate limiter and Prometheus metrics
rate_limiter = RateLimiter(limit=SMS_LIMIT_PER_MINUTE, interval=60)
sms_success_count = Counter('sms_success_count', 'Number of successful SMS sends')
sms_failure_count = Counter('sms_failure_count', 'Number of failed SMS sends')

# Start the Prometheus metrics server
start_http_server(8000)

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
            sms_success_count.inc()
            logging.info(f"SMS sent successfully to {phone_number} at {time.time()}")
            return True
        else:
            sms_failure_count.inc()
            logging.error(f"Failed to send SMS to {phone_number}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        sms_failure_count.inc()
        logging.error(f"Exception while sending SMS to {phone_number}: {e}")
    return False

def main():
    if rate_limiter.allow_send():
        success = send_sms(PHONE_NUMBER, PROXY_DETAILS)
        message = f"Sent SMS to {PHONE_NUMBER} via {OPERATOR} in {COUNTRY}" if success else f"Failed to send SMS to {PHONE_NUMBER}"
        print(message)
    else:
        print("Rate limit reached, waiting to send SMS...")
        rate_limiter.wait_until_allowed()

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
