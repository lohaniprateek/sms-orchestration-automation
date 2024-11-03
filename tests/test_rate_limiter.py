import unittest
import time
from rate_limiter import RateLimiter

class TestRateLimiter(unittest.TestCase):

    def setUp(self):
        # Set up a RateLimiter with a limit of 10 SMS per 1 minute for testing
        self.rate_limiter = RateLimiter(limit=10, interval=6)

    def test_allow_send_within_limit(self):
        # Should allow sending when within the rate limit
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())
        self.assertTrue(self.rate_limiter.allow_send())

    def test_disallow_send_exceeding_limit(self):
        # Exceeding the rate limit should disallow sending
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.assertFalse(self.rate_limiter.allow_send())  # 11th SMS should be disallowed

    def test_allow_send_after_interval_reset(self):
        # Exceeding limit initially, then allowing time for rate limiter to reset
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.assertFalse(self.rate_limiter.allow_send())  # Should be blocked

        # Wait for the interval to pass, so the limiter should allow sending again
        time.sleep(10)
        self.assertTrue(self.rate_limiter.allow_send())

    def test_wait_until_allowed(self):
        # Exceed the limit and then wait until allowed
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        self.rate_limiter.allow_send()
        start_time = time.time()
        
        # This call should block until the interval has passed
        self.rate_limiter.wait_until_allowed()
        end_time = time.time()

        # Confirm that at least the interval time has passed
        self.assertGreaterEqual(end_time - start_time, 6)
        self.assertTrue(self.rate_limiter.allow_send())

if __name__ == "__main__":
    unittest.main()
