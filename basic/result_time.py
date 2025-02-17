"""import matplotlib.pyplot as plt
# Python script to sum up times from lines starting with "real"
actual_values = [[0 for _ in range(10)] for _ in range(10)]

fig, ax = plt.subplots(figsize=(8, 7))

# Open the file in read mode
with open("class_test.txt", "r") as file:
    i = 1
    a = 0
    total_time = 0.0
    for line in file:
        # Process only lines that start with "real"
        if line.startswith("real"):
            i += 1
            # Extract the part after "m" and remove the "s" at the end
            # Example: line is "real    0m0.025s"
            time_str = line.split("m")[1].replace("s", "").strip()
            # Convert to float and add to the total
            if i == 10:
                actual_values[a][i-2] = float(time_str)
                i = 0
                a += 1
                total_time += float(time_str)
                print(f"Total time: {total_time/10} seconds")
                total_time = 0.0
            else:
                print(f"{a}:{i-1}{float(time_str)}")
                total_time += float(time_str)
                actual_values[a][i-2] = float(time_str)

import numpy as np
import matplotlib.pyplot as plt
print(actual_values)
# Given data
array_of_arrays = [
    "40 1400 100 20000",
    "40 1500 100 20000",
    "40 1600 100 20000",
    "40 1800 100 20000",
    "40 2000 100 20000",
    "40 2500 100 20000",
    "40 3000 100 20000",
    "40 4000 100 20000",
]

# Extract the second values as x
x_values = [int(line.split()[1]) for line in array_of_arrays]

"""
import numpy as np
import matplotlib.pyplot as plt 
from scipy import stats

x = np.array([1.5,2,2.5,3,3.5,4,4.5,5,5.5,6])
y = np.array([10.35,12.3,13,14.0,16,17,18.2,20,20.7,22.5])
gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
mn=np.min(x)
mx=np.max(x)
x1=np.linspace(mn,mx,500)
y1=gradient*x1+intercept
plt.plot(x,y,'ob')
plt.plot(x1,y1,'-r')
plt.show()