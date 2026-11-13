n = int(input("Enter array size: "))
arr = []

for i in range(n):
    val = int(input("Enter element: "))
    arr.append(val)
target = int(input("Enter target: "))
count = 0

for i in range(n):
    for j in range(i + 1, n):
        if arr[i] + arr[j] == target:
            count += 1
print("Number of pairs:", count)