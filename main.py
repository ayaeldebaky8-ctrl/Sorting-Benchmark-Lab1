import random
import time
import csv
import matplotlib.pyplot as plt


# 1. Insertion Sort
def insertion_sort(arr):
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


# 2. Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# 3. Quick Sort
def quick_sort(arr):
    arr = arr.copy()

    stack = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()

        if low >= high:
            continue

        pivot = arr[random.randint(low, high)]

        lt = low
        i = low
        gt = high

        while i <= gt:

            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1

            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1

            else:
                i += 1

        if low < lt - 1:
            stack.append((low, lt - 1))

        if gt + 1 < high:
            stack.append((gt + 1, high))

    return arr


# 4. Generate Data
def generate_data(size):

    sorted_data = list(range(size))

    reversed_data = sorted_data[::-1]

    random_data = [
        random.randint(0, size * 10)
        for _ in range(size)
    ]

    return {
        "Sorted": sorted_data,
        "Reversed": reversed_data,
        "Random": random_data
    }


# 5. Measure Execution Time
def measure_time(function, data):

    start = time.perf_counter()

    result = function(data)

    end = time.perf_counter()

    if result != sorted(data):
        raise ValueError("Incorrect sorting result")

    return end - start


# 6. Run Benchmark
def run_benchmark():

    sizes = [100, 500, 1000, 2000, 5000]

    algorithms = {
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Python sorted()": sorted
    }

    results = []

    for size in sizes:

        datasets = generate_data(size)

        for data_type, data in datasets.items():

            print("\nData:", data_type)
            print("Size:", size)

            for name, algorithm in algorithms.items():

                if (
                    name == "Insertion Sort"
                    and data_type != "Sorted"
                    and size > 2000
                ):
                    print(name, "Skipped")
                    continue

                elapsed = measure_time(algorithm, data)

                print(name, ":", round(elapsed, 6), "seconds")

                results.append([
                    name,
                    data_type,
                    size,
                    elapsed
                ])

    return results


# 7. Save Results
def save_results(results):

    with open(
        "benchmark_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Algorithm",
            "Data Type",
            "Size",
            "Execution Time"
        ])

        writer.writerows(results)


# 8. Create Charts
def create_charts(results):

    data_types = ["Sorted", "Reversed", "Random"]

    for data_type in data_types:

        plt.figure(figsize=(10, 6))

        algorithms = set(
            row[0] for row in results
            if row[1] == data_type
        )

        for algorithm in sorted(algorithms):

            selected = [
                row for row in results
                if row[0] == algorithm
                and row[1] == data_type
            ]

            selected.sort(key=lambda row: row[2])

            sizes = [row[2] for row in selected]
            times = [row[3] for row in selected]

            plt.plot(
                sizes,
                times,
                marker="o",
                label=algorithm
            )

        plt.title("Sorting Benchmark - " + data_type)
        plt.xlabel("Input Size")
        plt.ylabel("Execution Time (seconds)")
        plt.legend()
        plt.grid(True)

        plt.savefig(data_type.lower() + "_chart.png")
        plt.close()


# 9. Main
def main():

    print("SORTING BENCHMARK LAB")

    results = run_benchmark()

    save_results(results)

    create_charts(results)

    print("\nProject Completed Successfully!")


if __name__ == "__main__":
    main()
