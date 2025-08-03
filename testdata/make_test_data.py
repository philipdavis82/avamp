
def make_test_csv():
    import csv
    import os
    import random

    # Define the path for the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')

    # Sample data to write to the CSV file
    length = 1000
    dt     = 0.1
    data   = [['time','a','b','c']]
    for i in range(length):
        time = i * dt
        a = i * -2.0
        b = i *  3.0 + (i *  3.0 )*random.uniform(-0.1, 0.1)  # Adding some noise to 'b'
        c = i *  4.0 + random.uniform(-0.5, 0.5)  # Adding some noise to 'b'
        data.append([time, a, b, c])

    # Write data to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Test CSV file created at: {csv_file_path}")


if __name__ == "__main__":
    make_test_csv()
    print("Test data generation complete.")