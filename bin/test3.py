

from pprint import pprint
from yaml_manager import YamlManager

# Initialize with the test file
manager = YamlManager("source/benchmarks-addon.yaml")

print("--- Raw Data (manager.data) ---")
pprint(manager.data)

print("\n--- Flattened Data (manager.flat) ---")
pprint(manager.flat)

print("\n--- Iterating over manager.data ---")
for i, entry in enumerate(manager):
    print(f"Entry {i}: {entry.get('name', 'N/A')}")

print("\n--- Accessing by index (manager[0]) ---")
pprint(manager[0])

print("\n--- Length of manager (len(manager)) ---")
print(len(manager))

print("\n--- Getting entries by attribute ---")
compute_entries = manager.get_entries("details.category", "compute") # This requires 'details.category' to be a key in the raw data
                                                                    # if you're using self.data.
                                                                    # If you want to search flattened keys, you'd iterate manager.flat
print("Entries with category 'compute':")
pprint(compute_entries)

print("\n--- Getting entry by name ---")
benchmark2 = manager.get_by_name("MyBenchmark2")
print("Benchmark2 details:")
pprint(benchmark2)

#print("\n--- Checking URLs ---")
#manager.check_urls()

print("\n--- Checking Required Fields ---")
manager.check_required_fields()

print("\n--- Checking Filenames (name validation) ---")
manager.check_filenames()

print("\n--- Getting Citations ---")
citations = manager.get_citations()
pprint(citations)

