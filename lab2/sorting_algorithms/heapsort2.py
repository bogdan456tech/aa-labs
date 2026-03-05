def heapify(array,n,i):
    start = i

    while True:
        child = 2*i+1

        if child>=n:
            break
            
        if child+1<n and array[child]<array[child+1]:
            child+=1
        
        array[child],array[i] = array[i],array[child]

        i=child

    while i>start:
        parent = (i-1)//2

        if array[i]>array[parent]:
            array[i],array[parent] = array[parent],array[i]
            i = parent
        else:
            break

def heap_sort(array):
    n = len(array)

    for i in range(n//2-1,-1,-1):
        heapify(array,n,i)
    
    for i in range(n-1,0,-1):
        array[0],array[i] = array[i],array[0]
        heapify(array,i,0)
    
    return array
