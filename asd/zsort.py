arr= [5,2,4,6,1,3]
for i in range(1,len(arr)):
    j=i
    while j > 0 and arr[j-1] > arr[j]:
        arr[j-1] , arr[j] = arr[j] , arr[j-1]
        j=j-1
print(arr)