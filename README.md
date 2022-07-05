# TMXfolio
TMXfolio is an unofficial API to manage your portfolios on TMX.

It currently supports:
- Creating a portfolio
- Adding a symbol to a portfolio
- Adding a lot to a portfolio
- Deleting a portfolio
- Browsing your portfolios

## Installation
```properties
pip install -r requirements.txt
pip install -e .
```

## Usage
```python
import tmxfolio

manager = tmxfolio.Manager(authorization='?')

# Create a portfolio
myPortfolio = manager.create_portfolio('My Portfolio')

# Delete a portfolio by ID
manager.delete_portfolio(myPortfolio)

# List portfolios Names
portfolios = manager.get_portfolios()
for portfolio in portfolios:
    print("Portfolio: %s" % portfolio['name'])
```