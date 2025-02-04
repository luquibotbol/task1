import requests
import os
from dotenv import load_dotenv

# I wasn't able to get the price in SOL from just HELIUM RPC 
# I wasn't able to get the socials


# Load environment variables from .env file
load_dotenv()

# Get Helius API key from the environment
helius_api_key = os.getenv('HELIUS_API_KEY')

# Example Token Mint Address (replace with actual token mint)
token_mint = '6ogzHhzdrQr9Pgv6hZ2MNze7UrzBMAFyBBWUYp1Fhitx'

# Request
import requests

response = requests.post(
    "https://mainnet.helius-rpc.com/?api-key="+helius_api_key,
    json={"jsonrpc":"2.0","id":1,"method":"getAsset","params":{"id":"6ogzHhzdrQr9Pgv6hZ2MNze7UrzBMAFyBBWUYp1Fhitx"}}
)
data = response.json()

name = data['result']['content']['metadata']['name']
symbol = data['result']['content']['metadata']['symbol']
image = data['result']['content']['links']['image']
priceusd = data['result']['token_info']['price_info']['price_per_token']
supply = data['result']['token_info']['supply']/10**6


# print(data)



# Display Token Data
print("Name: ", name)
print("Symbol: ", symbol)
print("Image: ", image)
print("Supply:", supply)
print("Price: ", priceusd, " " + str(data['result']['token_info']['price_info']['currency']))
print("Market Cap:", priceusd*supply)
