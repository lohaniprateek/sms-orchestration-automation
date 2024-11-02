import time

class RateLimiter:
    def __init__(self, limit, interval):
        self.limit = limit            # Maximum SMS to send in the interval
        self.interval = interval      # Time interval in seconds
        self.timestamps = []          # Record of send times

    def allow_send(self):
        current_time = time.time()
        # Remove timestamps that are outside the interval
        self.timestamps = [t for t in self.timestamps if current_time - t < self.interval]

        if len(self.timestamps) < self.limit:
            # Allow sending and record the time
            self.timestamps.append(current_time)
            return True
        else:
            return False

    def wait_until_allowed(self):
        while not self.allow_send():
            time.sleep(1)  # Wait for a second and check again

# Usage example
if __name__ == "__main__":
    limiter = RateLimiter(limit=10, interval=60)  # 10 SMS per 60 seconds

    for _ in range(15):  # Try sending 15 messages
        if limiter.allow_send():
            print("SMS sent")
        else:
            print("Rate limit reached. Waiting...")
            limiter.wait_until_allowed()