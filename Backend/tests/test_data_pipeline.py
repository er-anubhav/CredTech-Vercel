import logging
from app.data.fetch_financials import save_company_and_financials
from app.data.fetch_news import fetch_and_store_news
from app.ml.scoring import score_company  # Assuming this function exists

def test_full_data_pipeline():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    tickers = ['AAPL', 'MSFT']
    for ticker in tickers:
        print(f"\n--- Testing pipeline for {ticker} ---")
        save_company_and_financials(ticker)
        try:
            result = score_company(ticker)
            print(f"Score for {ticker}: {result}")
        except Exception as e:
            print(f"Scoring failed for {ticker}: {e}")

if __name__ == "__main__":
    test_full_data_pipeline()
