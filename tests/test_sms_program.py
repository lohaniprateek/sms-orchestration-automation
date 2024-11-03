import unittest
from unittest.mock import patch, MagicMock
import sms_program

class TestSmsProgram(unittest.TestCase):

    @patch('sms_program.requests.post')
    @patch('sms_program.logging')
    def test_send_sms_success(self, mock_logging, mock_post):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call send_sms and check that it returns True
        result = sms_program.send_sms("1234567890", "http://proxy.example.com:8080")
        self.assertTrue(result)
        mock_logging.info.assert_called_with("SMS sent successfully to 1234567890 at", unittest.mock.ANY)

    @patch('sms_program.requests.post')
    @patch('sms_program.logging')
    def test_send_sms_failure(self, mock_logging, mock_post):
        # Mock a failed API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Call send_sms and check that it returns False
        result = sms_program.send_sms("1234567890", "http://proxy.example.com:8080")
        self.assertFalse(result)
        mock_logging.error.assert_called_with("Failed to send SMS to 1234567890. Status code: 500")

    @patch('sms_program.requests.post')
    def test_send_sms_exception(self, mock_post):
        # Simulate an exception being raised by requests.post
        mock_post.side_effect = Exception("Network Error")

        # Check that the program handles the exception and logs it
        with patch('sms_program.logging') as mock_logging:
            result = sms_program.send_sms("1234567890", "http://proxy.ePxample.com:8080")
            self.assertFalse(result)
            mock_logging.error.assert_called_with("Exception occurred while sending SMS to 1234567890: Network Error")

    @patch('sms_program.RateLimiter.allow_send', return_value=True)
    @patch('sms_program.send_sms', return_value=True)
    def test_main_sms_sent(self, mock_send_sms, mock_allow_send):
        # Test that main() sends an SMS if rate limiting allows it
        with patch('builtins.print') as mock_print:
            sms_program.main()
            mock_allow_send.assert_called_once()
            mock_send_sms.assert_called_once_with("1234567890", "http://proxy.example.com:8080")
            mock_print.assert_any_call("Sent SMS to 1234567890 via Operator1 in CountryA")

    @patch('sms_program.RateLimiter.allow_send', return_value=False)
    def test_main_rate_limited(self, mock_allow_send):
        # Test that main() waits if the rate limit is reached
        with patch('builtins.print') as mock_print:
            sms_program.main()
            mock_print.assert_any_call("Rate limit reached, waiting to send SMS...")

if __name__ == "__main__":
    unittest.main()
