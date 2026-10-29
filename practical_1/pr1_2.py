import pandas as pd
df = pd.DataFrame({
    "Name": ["Zunera","Alice", "Bob", "Charlie"],
    "city": ["Chicago","New York", "Los Angeles", "Chicago"],
    "Phone": ["555-555-5655","123-456-7890", "987-654-3210", "555-555-5555"],
    "Bill": [1800,1000, 2000, 1500]
})

print("Original DataFrame: \n", df)

print("\n Subset (Bill > 1000): \n ", df[df["Bill"] > 1000])

print("\n sorting (ascending) Bill: \n ",df.sort_values("Bill"))

print("\n sorting (descending) Bill: \n ",df.sort_values("Bill" , ascending=False))

print("\n Grouped by city : \n",df.groupby("city")["Bill"].mean())

print("\n mean: \n",df["Bill"].mean())

print("\n median: \n",df["Bill"].median())

print("\n mode: \n",df["Bill"].mode())