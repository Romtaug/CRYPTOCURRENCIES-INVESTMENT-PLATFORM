# Define a function to install and import a package
def install_and_import(package):
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} is not installed. Attempting installation...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} was successfully installed.")
        except Exception as e:
            print(f"Error during the installation of {package}: {e}")
            return None
    finally:
        # Attempt to import again after installation
        globals()[package] = __import__(package)

# List of all libraries needed
libraries = [
    're',  # For regular expressions
    'yfinance',  # For financial data
    'subprocess',  # Included as it's used within the script
    'sys',  # Also included for the same reason
    'matplotlib.pyplot',
    'datetime'
]

import matplotlib.pyplot as plt

print()
print("\n" + "-"*50 + "\n")
# Using the function to install and import each library
for library in libraries:
    install_and_import(library)

print("\n" + "-"*50 + "\n")

#####################################################################################################################

# Class to create a user account and manage portfolios
class UserAccount:
    def __init__(self, username, password, email, first_name=None, last_name=None):
        self.username = username
        self.__password = password  # Marked as private
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.portfolios = []  # Uses a list to manage multiple portfolios

    def set_username(self, new_username):
        self.username = new_username
    
    def set_password(self, new_password):
        self.__password = new_password
    
    def set_email(self, new_email):
        self.email = new_email
    
    def set_first_name(self, new_first_name):
        self.first_name = new_first_name
    
    def set_last_name(self, new_last_name):
        self.last_name = new_last_name
    
    def add_portfolio(self, new_portfolio):
        # Checks if a portfolio with the same name already exists
        if any(p.name == new_portfolio.name for p in self.portfolios):
            print(f"A portfolio named '{new_portfolio.name}' already exists for user {self.username}.")
            return False  # Indicates the portfolio was not added
        # Adds the new portfolio to the list
        self.portfolios.append(new_portfolio)
        print(f"Portfolio '{new_portfolio.name}' added successfully for user {self.username}.")
        return True  # Indicates the portfolio was successfully added

    def remove_portfolio(self, portfolio_to_remove):
        # Searches the portfolio by its name
        for idx, portfolio in enumerate(self.portfolios):
            if portfolio.name == portfolio_to_remove.name:
                del self.portfolios[idx]  # Removes the portfolio from the list
                print(f"The portfolio '{portfolio_to_remove.name}' was successfully removed.")
                return True  # Indicates the portfolio was successfully removed
        print(f"No portfolio named '{portfolio_to_remove.name}' found.")
        return False  # Indicates the portfolio was not found and thus not removed
    
    def view_total_liquidity(self):
        total_liquidity = sum(portfolio.liquidity for portfolio in self.portfolios)
        return total_liquidity
    
    def get_user_info(self):
        info = f"Username: {self.username}, Email: {self.email}, First Name: {self.first_name}, Last Name: {self.last_name}"
        if self.portfolios:
            info += "\nPortfolios:"
            for portfolio in self.portfolios:
                info += f"\n- {portfolio.name}"
            total_liquidity = self.view_total_liquidity()
            info += f"\nTotal liquidity available across all portfolios: {total_liquidity} USD"
        else:
            info += "\nNo portfolio created."
        
        print(info)
        return info

"""
user1 = UserAccount("johnDoe123", "supersecretpassword", "johndoe@example.com", "John", "Doe")
print(user1.get_user_info())

Updating user information
user1.set_email("newemail@example.com")
user1.set_first_name("Johnny")
user1.set_last_name("Doe II")
print(user1.get_user_info())
"""

################################################################################################################################################################

# Remplacer 'BTC-USD' par le ticker de votre choix
"""
ticker = yfinance.Ticker("BTC-USD")
info = ticker.info
Imprime toutes les clés et leurs valeurs associées
for key, value in info.items():
   print(f"{key}: {value}")
"""
    
class Crypto:
    def __init__(self, ticker):
        self.ticker = ticker
        self.info = None
        self.load_info()

    def load_info(self):
        """Loads cryptocurrency information from Yahoo Finance."""
        try:
            self.info = yfinance.Ticker(self.ticker).info
        except Exception as e:
            print(f"Error loading information for {self.ticker}: {e}")

    def get_price_close(self):
        """Returns the current price."""
        return self.info.get('previousClose') if self.info else None

    def get_volume(self):
        """Returns the current volume."""
        return self.info.get('regularMarketVolume') if self.info else None
    
    def get_market_cap(self):
        """Returns the market cap."""
        return self.info.get('marketCap') if self.info else "Market cap information not available."


    def get_description(self):
        """Returns the description."""
        return self.info.get('description') if self.info else None

    def extract_price_from_description(self):
        """Extracts the price from the description."""
        description = self.get_description()
        if description:
            match = re.search(r"The last known price of Bitcoin is ([\d,]+.\d+) USD", description)
            if match:
                return match.group(1)
            else:
                return "Price not found in description."
        else:
            return "Description not available."

    def analyze_investment_opportunity(self):
        # Get today's date in YYYY-MM-DD format
        today = datetime.date.today()
        today_str = today.strftime('%Y-%m-%d')

        # Download historical data for the specified ticker
        data = yfinance.download(self.ticker, start="2020-01-01", end=today_str)
        
        # Calculate moving averages for 120 and 240 days
        data['MA120'] = data['Adj Close'].rolling(window=120).mean()
        data['MA240'] = data['Adj Close'].rolling(window=240).mean()

        # Investment decision based on moving averages
        try:
            last_MA120 = data['MA120'].iloc[-1]
            last_MA240 = data['MA240'].iloc[-1]
            if last_MA120 > last_MA240:
                decision = "It's a good time to invest because MA120 > MA240."
            else:
                decision = "It's not a favorable time to invest because MA120 < MA240."
        except IndexError:
            decision = "Insufficient data to make an investment decision."

        # Display the chart
        plt.figure(figsize=(14, 7))
        plt.plot(data['Adj Close'], label='Adjusted Close Price', color='blue')
        plt.plot(data['MA120'], label='MA 120 days', color='green', linestyle='--')
        plt.plot(data['MA240'], label='MA 240 days', color='red', linestyle='--')
        plt.title(f'Bitcoin Price Analysis with MA120 and MA240\n{decision}')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.legend()
        plt.show()

        return decision
        
########################################################################################################################

class Bitcoin(Crypto):
    def __init__(self):
        super().__init__('BTC-USD')

tickers = [
    'BTC-USD',  # Bitcoin
    'ETH-USD',  # Ethereum
    'BNB-USD',  # Binance Coin
    'XRP-USD',  # XRP
    'SOL-USD',  # Solana
    'ADA-USD',  # Cardano
    'DOT-USD',  # Polkadot
    'DOGE-USD', # Dogecoin
    'LTC-USD',  # Litecoin
    'LINK-USD'  # Chainlink
]

# Processing information for each cryptocurrency

for ticker in tickers:
    crypto = Crypto(ticker)
    # Example code for processing each cryptocurrency's data would go here


    """
    print(f"{ticker} Price Close: {crypto.get_price_close()} USD")
    print(f"{ticker} Volume: {crypto.get_volume()}")
    # print(f"{ticker} Description: {crypto.get_description()}")
    print(f"{ticker} Market Cap: {crypto.get_market_cap()} USD")
    print("\n" + "-"*50 + "\n")
    """

#######################################################################################################

class Portfolio:
    def __init__(self, name):
        self.name = name
        self.liquidity = 0
        self.crypto_balances = {}
        self.transaction_history = [] 
    
    def set_name(self, new_name):
        self.name = new_name
        print(f"The portfolio's name has been changed to '{new_name}'.")

    def view_transaction_history(self):
        if self.transaction_history:
            print("Transaction history:")
            for transaction in self.transaction_history:
                print(transaction)
        else:
            print("No transactions have been made.")

    def get_portfolio_info(self):
        info = f"Portfolio Name: {self.name}\nAvailable Liquidity: {self.liquidity} USD\n"
        if self.crypto_balances:
            info += "Cryptocurrency Balances:\n"
            for ticker, quantity in self.crypto_balances.items():
                info += f"  {ticker}: {quantity}\n"
        else:
            info += "No cryptocurrencies in this portfolio.\n"
        info += "\nTransaction History:\n" + ("\n".join(self.transaction_history) if self.transaction_history else "No transactions made.")
        print(info)

    def add_liquidity(self):
        amount = input("How much would you like to add to the liquidity? ")
        try:
            amount = float(amount)
            if amount > 0:
                self.liquidity += amount
                self.transaction_history.append(f"Added {amount} USD to liquidity.")
                print(f"{amount} USD added to liquidity. Total liquidity: {self.liquidity} USD.")
            else:
                print("Please enter a positive amount.")
        except ValueError:
            print("Please enter a valid number.")

    def withdraw_liquidity(self):
        amount = input("How much would you like to withdraw from the liquidity? ")
        try:
            amount = float(amount)
            if amount > 0 and self.liquidity >= amount:
                self.liquidity -= amount
                self.transaction_history.append(f"Withdrew {amount} USD from liquidity.")
                print(f"{amount} USD withdrawn from liquidity. Remaining liquidity: {self.liquidity} USD.")
            elif amount <= 0:
                print("Please enter a positive amount.")
            else:
                print("Insufficient balance.")
        except ValueError:
            print("Please enter a valid number.")

    def view_balances(self):
        print(f"Available Liquidity: {self.liquidity} USD")
        print("Cryptocurrency Balances:")
        for ticker, quantity in self.crypto_balances.items():
            print(f"  {ticker}: {quantity}")

    def buy_crypto(self):
        available_tickers = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'SOL-USD', 'ADA-USD', 'DOT-USD', 'DOGE-USD', 'LTC-USD', 'LINK-USD']
        while True:
            ticker = input(f"Which crypto would you like to buy from {', '.join(available_tickers)}? Enter the ticker or 'cancel' to exit: ").strip()
            if ticker == 'cancel':
                print("Operation cancelled.")
                break
            if ticker not in available_tickers:
                print("This ticker is not in the list of available cryptos. Please try again or cancel.")
                continue

            try:
                total_amount = float(input("Enter the total amount in USD you wish to spend: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            crypto = Crypto(ticker)
            current_price = crypto.get_price_close()
            if current_price is None:
                print(f"Unable to retrieve the current price for {ticker}. Please try again.")
                continue

            fee = total_amount * 0.005  # Platform's fee calculation
            amount_after_fees = total_amount - fee  # Actual amount to use for the purchase

            if self.liquidity >= total_amount:
                purchasable_quantity = amount_after_fees / current_price
                self.crypto_balances[ticker] = self.crypto_balances.get(ticker, 0) + purchasable_quantity
                self.liquidity -= total_amount  # Deduct the total amount including fees
                Platform.collect_fees(fee)  # Correctly calls collect_fees to add the fee to the platform's total fees
                print(f"Purchase successful: {purchasable_quantity} of {ticker} for {amount_after_fees} USD (5% fee included).")
                print(f"Remaining liquidity: {self.liquidity} USD.")
                break
            else:
                print("Purchase failed. Insufficient liquid balance.")
                break


    def sell_crypto(self):
        if not self.crypto_balances:
            print("Your cryptocurrency portfolio is empty.")
            return

        while True:
            print("Cryptos available to sell in your portfolio:")
            for ticker, quantity in self.crypto_balances.items():
                print(f"{ticker}: {quantity}")

            ticker = input("Enter the ticker of the crypto you wish to sell or 'cancel' to exit: ").strip()

            if ticker.lower() == 'cancel':
                print("Operation cancelled.")
                break

            if ticker not in self.crypto_balances:
                print("This ticker is not present in your portfolio. Please try again.")
                continue

            quantity_to_sell = self.crypto_balances[ticker]

            crypto = Crypto(ticker)
            current_price = crypto.get_price_close()
            if current_price is None:
                print(f"Unable to retrieve the current price for {ticker}. Please try again.")
                continue

            amount_received = quantity_to_sell * current_price
            self.liquidity += amount_received
            del self.crypto_balances[ticker]
            print(f"Sale successful: You sold {quantity_to_sell} {ticker} for a total of {amount_received} USD.")
            self.transaction_history.append(f"Sale of {quantity_to_sell} {ticker} received {amount_received} USD.")
            print(f"Remaining liquidity: {self.liquidity} USD.")  # Displays the remaining liquidity after the sale
            break


#####################################################################################################################################

class Platform:
    _instance = None
    total_fees = 0  # Tracking the total fees accumulated by the platform

    def __new__(cls, name, siret, location):
        if cls._instance is None:
            cls._instance = super(Platform, cls).__new__(cls)
            cls._instance.name = name
            cls._instance.siret = siret
            cls._instance.location = location
            cls._instance.users = []
        return cls._instance

    @classmethod
    def collect_fees(cls, fees):
        cls.total_fees += fees
        print(f"Fees of {fees} USD added. Total fees accumulated: {cls.total_fees} USD.")

    def add_user(self, user):
        self.users.append(user)
        print(f"User {user.username} added to the platform.")

    def remove_user(self, user):
        self.users = [u for u in self.users if u.username != user.username]
        print(f"User {user.username} removed from the platform.")

    @classmethod
    def pay_taxes(cls):
        taxes = cls.total_fees * 0.30
        cls.total_fees -= taxes
        print(f"Taxes of {taxes} USD paid. Remaining fees: {cls.total_fees} USD.")

# Example of use
#################################################################################################################################
platform = Platform("CryptoPlatform", 36252187900034, "Vilnius")
#################################################################################################################################    
user1 = UserAccount("romTaug20", "IloveVilniusTech$$", "romtaug@gmail.com", "Romain", "Taugourdeau")
platform.add_user(user1)
user1.get_user_info()
###########################################################################################################################
print()
wallet1 = Portfolio("wallet1")
wallet2 = Portfolio("wallet2")

user1.add_portfolio(wallet1)
user1.get_user_info()
print()
user1.add_portfolio(wallet2)
user1.get_user_info()
print()
user1.remove_portfolio(wallet2)
user1.get_user_info()
####################################################################################################################################
print()
wallet1.add_liquidity()
print()
########################################################################################################################################
# Create an instance for Bitcoin
crypto_btc = Crypto("BTC-USD")
investment_decision = crypto_btc.analyze_investment_opportunity()
######################################################################################################################################
print(investment_decision)
wallet1.buy_crypto()
wallet1.buy_crypto()
print()
wallet1.sell_crypto()
wallet1.sell_crypto()
print()
wallet1.view_balances()
print()
wallet1.view_transaction_history()
wallet1.view_balances()
#####################################################################################################################################
# Displaying total fees
print()
print(f"Total fees accumulated on the platform: {Platform.total_fees} USD")

# Paying taxes
platform.pay_taxes()

# Displaying remaining fees after tax payment
print(f"Remaining fees after taxes: {Platform.total_fees} USD")