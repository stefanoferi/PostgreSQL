import os

# Get environment variables
USER = os.getenv('API_USER')

print('Hello world, ' + USER)