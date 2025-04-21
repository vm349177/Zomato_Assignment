import pandas as pd
import os

def reformat_to_standard_csv(input_csv):
    # Define required columns
    target_columns = [
        "restaurant", "category", "item_name", "description",
        "options", "tags", "spice_level", "state", "address", "contact_info"
    ]

    # Load input CSV
    df = pd.read_csv(input_csv)

    # Clean column names
    df.columns = [col.lower().strip() for col in df.columns]

    # Optional renaming if user has used variations
    column_map = {
        "name": "item_name",
        "item": "item_name",
        "menu_item": "item_name"
    }
    df.rename(columns=column_map, inplace=True)

    # Ensure all target columns exist
    for col in target_columns:
        if col not in df.columns:
            df[col] = ""

    # Reorder + clean
    df = df[target_columns]
    df.fillna("", inplace=True)

    # Generate output file name
    input_base = os.path.basename(input_csv)
    output_name = f"formatted_{input_base}"
    df.to_csv(output_name, index=False)

    print(f"✅ Reformatted CSV saved as: {output_name}")

reformat_to_standard_csv("products_nasha.csv")
