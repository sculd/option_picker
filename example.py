import http.client as httplib
import os

# Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)

_ACCESS_TOKEN_TRADIER = os.environ['TRADIER_ACCESS_TOKEN']

connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

# Headers
headers = {"Accept":"application/json",
           "Authorization":"Bearer " + _ACCESS_TOKEN_TRADIER}

# Send synchronously
connection.request('GET', '/v1/markets/quotes?symbols=spy', None, headers)
try:
  response = connection.getresponse()
  content = response.read()
  # Success
  print('Response status ' + str(response.status))
except httplib.HTTPException as e:
  # Exception
  print('Exception during request')
