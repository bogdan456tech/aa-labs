def heapify(array,n,i):
    l = 2*i+1
    r = 2*i+2

    largest=i

    if l<n and array[l]>array[largest]:
        largest=l
    
    if r<n and array[r]>array[largest]:
        largest=r
    
    if largest!=i:
        array[i],array[largest] = array[largest],array[i]
        heapify(array,n,largest)

    
def heap_sort(array):
    n = len(array)

    for i in range(n//2-1,-1,-1):
        heapify(array,n,i)
    
    for i in range(n-1,0,-1):
        array[0],array[i] = array[i],array[0]
        heapify(array,i,0)

    return array