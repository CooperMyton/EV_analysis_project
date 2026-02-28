import sys
import pandas as pd

''' Strips leading or trailing white space off of column headers '''

def main():
    if len(sys.argv) != 3:
        print("Usage: python strip_headers.py <input_csv> <output_csv>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading input CSV: {e}")
        sys.exit(1)

    print("\nOriginal Columns:")
    print(", ".join(df.columns))

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    print("\nCleaned Columns:")
    print(", ".join(df.columns))

    try:
        df.to_csv(output_path, index=False)
        print(f"\nCleaned CSV saved to: {output_path}")
    except Exception as e:
        print(f"Error writing output CSV: {e}")

if __name__ == "__main__":
    main()