from yahoo_finance import Share

# Ask for user input of stock ticker
# Prints out company name and current price
def main():

    ticker = str(raw_input("Stock Ticker: "))

    company = Share(ticker)

    company.refresh()

    print company.get_name()
    print "Current Price: ", company.get_price()

if __name__ == "__main__":
    main()