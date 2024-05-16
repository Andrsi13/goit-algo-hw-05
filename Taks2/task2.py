def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0
    
    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid]
        
        if mid_val < target:
            low = mid + 1
        elif mid_val > target:
            high = mid - 1
        else:
            return (iterations, mid_val)
        
        iterations += 1
    
    if high < 0:
        return (iterations, None)
    else:
        return (iterations, arr[low])

# Приклад використання:
arr = [0.1, 0.3, 0.5, 0.7, 0.9]
target = 0.6
result = binary_search(arr, target)
print("Кількість ітерацій:", result[0])
print("Верхня межа:", result[1])
