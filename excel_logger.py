import pandas as pd
from settings import EXCEL_LOG_PATH

def log_to_excel(data):
    df = pd.DataFrame(data)
    try:
        existing_df = pd.read_excel(EXCEL_LOG_PATH)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_excel(EXCEL_LOG_PATH, index=False)
    print(f"Log written to {EXCEL_LOG_PATH}")
