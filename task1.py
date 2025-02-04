import requests

# Helius API Setup
helius_api_key = 'YOUR_HELIUS_API_KEY'
helius_url = f"https://api.helius.xyz/v0/token-metadata?api-key={helius_api_key}"

# Jupiter API Setup
jupiter_url = "https://quote-api.jup.ag/v4/price"

# Example Token Mint Address (replace with actual token address)
token_mint = 'TOKEN_MINT_ADDRESS'

# Fetch Token Metadata from Helius
metadata_response = requests.get(f"{helius_url}&mint={token_mint}")
metadata = metadata_response.json()

# Fetch Token Price from Jupiter
price_response = requests.get(f"{jupiter_url}?ids={token_mint}")
price_data = price_response.json()

# Display Data
print("Name:", metadata.get('name'))
print("Symbol:", metadata.get('symbol'))
print("Image:", metadata.get('logoURI'))
print("Price in SOL:", price_data['data']['priceInSOL'])
print("Price in USD:", price_data['data']['priceInUSD'])
print("Social Links:", metadata.get('socials', 'N/A'))
print("Supply:", metadata.get('supply'))
print("Market Cap / FDV:", metadata.get('marketCap'))
