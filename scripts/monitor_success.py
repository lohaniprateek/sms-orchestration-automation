import json
import time
import logging
import os

# Path to config.json
CONFIG_PATH = "config/config.json"
LOG_FILE_PATH = "logs/sms_log.log"
SUCCESS_THRESHOLD = 0.9  # Success rate threshold to consider a pair successful

# Configure logging for monitoring
logging.basicConfig(filename='logs/monitor_log.log', level=logging.INFO)

def load_config():
    with open(CONFIG_PATH, 'r') as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_PATH, 'w') as file:
        json.dump(config, file, indent=4)

def calculate_success_rate(log_file_path, country, operator):
    total_sms = 0
    successful_sms = 0

    # Read the log file to calculate success rate
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if f"{country}" in line and f"{operator}" in line:
                total_sms += 1
                if "SMS sent successfully" in line:
                    successful_sms += 1

    return successful_sms / total_sms if total_sms > 0 else 0

def update_config_based_on_success():
    config = load_config()
    updated_pairs = []

    # Update each country-operator pair based on success rate
    for country_data in config["country_operator_pairs"]:
        country = country_data["country"]
        for operator_data in country_data["operators"]:
            operator = operator_data["name"]
            success_rate = calculate_success_rate(LOG_FILE_PATH, country, operator)
            
            if success_rate >= SUCCESS_THRESHOLD:
                updated_pairs.append((country, operator))
                logging.info(f"{country}-{operator} pair retained with success rate: {success_rate}")
            else:
                logging.info(f"{country}-{operator} pair dropped due to low success rate: {success_rate}")

    # Save updated pairs back to config
    config["country_operator_pairs"] = [
        {
            "country": pair[0],
            "operators": [{"name": pair[1]}]
        }
        for pair in updated_pairs
    ]

    save_config(config)

if __name__ == "__main__":
    while True:
        update_config_based_on_success()
        logging.info("Config updated based on success rates.")
        time.sleep(3600)  # Run every hour