import os
import sys

variables = ['API_PORT', 'ENV']

if os.environ['ENV'] == "dev":
    origins = ["*"]
else:
    origins = ["*"]

api_cors_config = {
    "origins": origins,
    "methods": ["OPTIONS", "GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type"]
}

def checkEnv():
    for variable in variables:
        if variable not in os.environ:
            print(str(variable) + " environment variable not found")
            sys.exit()