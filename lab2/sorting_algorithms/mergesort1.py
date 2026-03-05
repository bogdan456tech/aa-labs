def merge(array,l,m,r):
    n1 = m-l+1
    n2 = r-m

    L = [0]*n1
    R = [0]*n2

    for i in range(n1):
        L[i]=array[l+i]
    for j in range(n2):
        R[j]=array[m+1+j]
    
    i = j = 0
    k = l

    while i<n1 and j<n2:
        if L[i]<R[j]:
            array[k]=L[i]
            i+=1
        else:
            array[k]=R[j] 
            j+=1

        k+=1
    
    while i<n1:
        array[k]=L[i]
        i+=1
        k+=1
    
    while j<n2:
        array[k]=R[j]
        j+=1
        k+=1

def mergesort(array,l,r):
    if l<r:
        m = l + (r-l)//2


        mergesort(array,l,m)
        mergesort(array,m+1,r)

        merge(array,l,m,r)

def start_merge_sort(array):
    if len(array) > 1:
        mergesort(array, 0, len(array) - 1)
    return array
