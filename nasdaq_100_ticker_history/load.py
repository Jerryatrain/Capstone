import yaml
import datetime
import os

def get_nasdaq100_tickers(date_str):
    """
    Determine the Nasdaq 100 tickers for a given date based on YAML files.
    
    Args:
        date_str (str): The date in 'YYYY-MM-DD' format (e.g., '2024-03-18').
    
    Returns:
        list: A sorted list of ticker symbols representing the Nasdaq 100 composition on the given date.
    
    Raises:
        FileNotFoundError: If the YAML file for the specified year is not found.
        ValueError: If the date string is not in the correct format.
    """
    # Parse the input date
    try:
        input_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Date must be in 'YYYY-MM-DD' format.")
    
    year = input_date.year
    
    # Construct the file name based on the year
    file_name = os.path.join(os.path.dirname(__file__), f"n100-ticker-changes-{year}.yaml")
    
    # Check if the YAML file exists
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"YAML file 'n100-ticker-changes-{year}.yaml' not found.")
    
    # Load the YAML file
    with open(file_name, 'r') as f:
        data = yaml.safe_load(f)
    
    # Extract the initial tickers from January 1st
    initial_tickers = data['tickers_on_Jan_1']

    # replace True by 'ON'
    initial_tickers = [ticker if ticker!=True else 'ON' for ticker in initial_tickers ]
    
    # Extract the changes dictionary, default to empty dict if no changes
    changes = data.get('changes', {})
    
    # Initialize a set with the initial tickers
    tickers_set = set(initial_tickers)
    
    # Collect change dates that are on or before the input date
    applicable_change_dates = [
        change_date_str
        for change_date_str in changes.keys()
        if datetime.datetime.strptime(change_date_str, '%Y-%m-%d') <= input_date
    ]
    
    # Sort the change dates chronologically
    applicable_change_dates.sort()
    
    # Apply each change in chronological order
    for change_date_str in applicable_change_dates:
        change = changes[change_date_str]
        # Remove tickers listed in 'difference'
        for ticker in change.get('difference', []):
            tickers_set.discard(ticker)
        # Add tickers listed in 'union'
        for ticker in change.get('union', []):
            tickers_set.add(ticker)
    
    # Return the tickers as a sorted list
    return sorted(tickers_set)

# Example usage
if __name__ == "__main__":
    # Test cases based on the 2024 YAML example
    test_dates = [
        '2024-01-01',  # Before any changes
        '2024-03-18',  # On the first change date
        '2024-07-22',  # After multiple changes
        '2024-12-31',  # After all changes
    ]
    
    for date in test_dates:
        
        try:
            tickers = get_nasdaq100_tickers(date)
            print(f"Tickers on {date} {len(tickers)}: {tickers}")
        except Exception as e:
            print(f"Error for {date}: {e}")