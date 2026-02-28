import sys
import pandas as pd

''' Takes input fie patha dn output file path. Prints column headers of input, and prompts for
    desired columns to remove. Saves csv with removed columns to output file path. '''

def main():
    if len(sys.argv) != 3:
        print("Usage: python remove_columns.py <input_csv> <output_csv>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading input CSV: {e}")
        sys.exit(1)

    # Print columns as comma-separated values
    print("\nColumns in CSV:")
    print(", ".join(df.columns))

    cols_to_remove = input("\nEnter comma-separated column names to remove: ")

    # Clean user input
    cols_to_remove = [col.strip() for col in cols_to_remove.split(",") if col.strip()]

    # Filter valid/invalid columns
    valid_cols = [col for col in cols_to_remove if col in df.columns]
    invalid_cols = [col for col in cols_to_remove if col not in df.columns]

    if invalid_cols:
        print(f"\nWarning: These columns were not found and will be ignored: {invalid_cols}")

    df = df.drop(columns=valid_cols)

    try:
        df.to_csv(output_path, index=False)
        print(f"\nModified CSV saved to: {output_path}")
    except Exception as e:
        print(f"Error writing output CSV: {e}")

if __name__ == "__main__":
    main()