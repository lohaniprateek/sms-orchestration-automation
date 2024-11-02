# Official lightweight Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Set environment variables
ENV COUNTRY=default_country
ENV OPERATOR=default_operator
ENV PHONE_NUMBER=default_phone
ENV PROXY_DETAILS=default_proxy

# Expose a port for Prometheus or other monitoring tools)
EXPOSE 8000

# Run the main SMS program
CMD ["python", "scripts/sms_program.py"]
