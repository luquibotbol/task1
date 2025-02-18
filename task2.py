import requests
import os
from dotenv import load_dotenv
import tabulate

try:
    from tabulate import tabulate
    use_tabulate = True
except ImportError:
    use_tabulate = False
    

def get_assets_by_owner(api_key, owner_address, page=1, limit=1000, display_options=None):
    url = f"https://mainnet.helius-rpc.com/?api-key={api_key}"
    
    # Base payload for the JSON-RPC call
    payload = {
        "jsonrpc": "2.0",
        "id": "python-example",
        "method": "getAssetsByOwner",
        "params": {
            "ownerAddress": owner_address,
            "page": page,
            "limit": limit,
        }
    }
    
    # Optionally add display options to include extra data (e.g., fungible tokens, native balance)
    if display_options:
        payload["params"]["displayOptions"] = display_options
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

def format_tokens_with_prices(assets_items):
    tokens = []
    for asset in assets_items:
        if asset.get("interface") == "FungibleToken":
            content = asset.get("content", {})
            metadata = content.get("metadata", {})
            token_name = metadata.get("name", "Unknown")
            token_symbol = metadata.get("symbol", "Unknown")
            
            token_info = asset.get("token_info", {})
            balance = token_info.get("balance", 0)
            price_info = token_info.get("price_info", {})
            price_per_token = price_info.get("price_per_token", "N/A")
            total_price = price_info.get("total_price", "N/A")
            
            tokens.append({
                "Token Name": token_name,
                "Symbol": token_symbol,
                "Balance": balance,
                "Price per Token": price_per_token,
                "Total Price": total_price
            })
    return tokens


def calculate_cumulative_value(assets, sol_usd_rate=None):
    tokens = format_tokens_with_prices(assets.get("items", []))
    cumulative_token_usd = 0.0
    for token in tokens:
        # Only add if a valid numeric total price is available
        if token["Total Price"] != "N/A":
            cumulative_token_usd += token["Total Price"]
    
    native_sol = 0.0
    native_sol_usd = 0.0
    sol_usd_rate = assets["nativeBalance"].get("price_per_sol", 1)
    if "nativeBalance" in assets:
        native_balance = assets["nativeBalance"].get("lamports", 0)
        # Convert lamports to SOL (1 SOL = 1e9 lamports)
        native_sol = native_balance / 1e9
        if sol_usd_rate is not None:
            native_sol_usd = native_sol * sol_usd_rate
    
    cumulative_total_usd = cumulative_token_usd + native_sol_usd
    return native_sol, native_sol_usd, cumulative_token_usd, cumulative_total_usd


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get Helius API key from the environment
    api_key = os.getenv('HELIUS_API_KEY')
    owner_address = "B8yQuZiC4Ku6VNuGDLRrUQnVRC4LJFnzGVUC6ArrMk51"
    
    # Display options: here we ensure fungible tokens are returned (and native balance if needed)
    display_options = {
        "showFungible": True,
        "showNativeBalance": True
    }
    
    results = get_assets_by_owner(api_key, owner_address, display_options=display_options)
    print(results)
    assets = results.get("result", {})
    if assets:
        tokens_data = format_tokens_with_prices(assets.get("items", []))
        if tokens_data:
            if use_tabulate:
                print(tabulate(tokens_data, headers="keys", tablefmt="grid"))
            else:
                for token in tokens_data:
                    if token["Total Price"] != "N/A":
                        print(f"Token: {token['Token Name']} ({token['Symbol']})")
                        print(f"Balance: {token['Balance']}")
                        print(f"Price per Token: {token['Price per Token']}")
                        print(f"Total Price: {token['Total Price']}")
                        print("-" * 40)
        else:
            print("No fungible tokens found with price info.")
    else:
        print("No assets retrieved.")

    sol_usd_rate = 25.0
    
    native_sol, native_sol_usd, tokens_usd, cumulative_total_usd = calculate_cumulative_value(assets, sol_usd_rate)
    
    print("\nAccount Summary:")
    print(f"Native SOL Balance: {native_sol:.4f} SOL (≈ ${native_sol_usd:,.2f} USD)")
    print(f"Fungible Tokens Total USD Value: ${tokens_usd:,.2f}")
    print(f"Cumulative Total USD Value: ${cumulative_total_usd:,.2f}")


if __name__ == "__main__":
    main()