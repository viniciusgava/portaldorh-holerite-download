import os
import sys

if os.environ.get('RH_USERNAME') is None:
    sys.exit("Missing ENV VARIABLE RH_USERNAME")

if os.environ.get('RH_PASSWORD') is None:
    sys.exit("Missing ENV VARIABLE RH_PASSWORD")

# customer username
username = os.environ.get('RH_USERNAME')

# Customer Password
password = os.environ.get('RH_PASSWORD')
