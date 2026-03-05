def merge(array,l,m,r):
    p1 = m-l+1
    p2 = r-m

    L = [0]*p1
    R = [0]*p2

    for i in range(p1):
        L[i]=array[l+i]
    for j in range(p2):
        R[j] = array[m+1+j]
    
    i = j = 0
    k = l

    while i<p1 and j<p2:
        if L[i]<=R[j]:
            array[k]=L[i]
            i+=1
        else:
            array[k]=R[j]
            j+=1
        k+=1
    
    while i<p1:
        array[k]=L[i]
        i+=1
        k+=1
    
    while j<p2:
        array[k]=R[j]
        j+=1
        k+=1
    
def mergesort(array,l,r):
    if l<r:
        
        m = l+(r-l)//2

        mergesort(array,l,m)
        mergesort(array,m+1,r)

        if array[m]<=array[m+1]:
            return
        
        merge(array,l,m,r)


def start_merge_sort(array):
    if len(array) > 1:
        mergesort(array, 0, len(array) - 1)
    return array
