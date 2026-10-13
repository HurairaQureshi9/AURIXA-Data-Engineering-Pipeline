
from load import prepare_datasets, validate_relationships


def main():
    print("\nAURIXA ETL VALIDATION TEST")
    print("=" * 40)

    datasets = prepare_datasets()
    validate_relationships(datasets)

    print("\nAll source validations passed!")
    print("\nDataset row counts:")

    for table, df in datasets.items():
        print(f"{table}: {len(df):,} rows")

    print("\nPASS: All 9 datasets passed validation.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nVALIDATION FAILED: {error}")
        raise
