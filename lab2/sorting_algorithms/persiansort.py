def jumpinsert(ar, start, i, aux, aux_start, j):
    jump = j - aux_start + 1
    
    while j >= aux_start:
        temp = aux[j]
        while i >= start and ar[i] > temp:
            ar[i + jump] = ar[i]
            i -= 1
        
        ar[i + jump] = temp
        jump -= 1
        j -= 1

def auxiliary_size(n, wp):
    m = n // wp
    if m == 0:
        return 2
    else:
        return 1 + m + auxiliary_size(m, wp)

def reverse_segment(ar, s, e):
    while s < e:
        ar[s], ar[e] = ar[e], ar[s]
        s += 1
        e -= 1

def warping(ar, aux, start, end, aux_size, wp):
    if start >= end:
        return

    max_jump = ((end - start + 1) // wp) + 1
    i = start

    while i < end and ar[i + 1] < ar[i]:
        i += 1
    if i > start:
        reverse_segment(ar, start, i)


    while i < end:
        while i < end and ar[i + 1] >= ar[i]:
            i += 1
        
        if i == end:
            return

        if (i + max_jump) > end:
            max_jump = end - i

        if (end - start + 1) > aux_size:
            for j in range(1, max_jump + 1):
                aux[j] = ar[i + j]
            
            if max_jump > 1:
                warping(aux, aux, 1, max_jump, aux_size, wp)
            
            jumpinsert(ar, start, i, aux, 1, max_jump)
            i = i + max_jump
            
        else:
            temp = end - i
            low = end + 1
            high = end + max_jump
            
            if high >= len(aux):
                aux.extend([0] * (high - len(aux) + 1))

            for j in range(low, high + 1):
                aux[j] = ar[j - temp]
            
            if max_jump > 1:
                warping(aux, aux, low, high, aux_size, wp)
            
            jumpinsert(ar, start, i, aux, low, high)
            i = i + max_jump

def persiansort(ar, wp=9):
    n = len(ar)
    if n <= 1: return ar
    
    start = 0
    end = n - 1
    aux_s = auxiliary_size(n, wp)
    
    if (end - start + 1) < wp:
        aux_s = 1
        
    aux = [0] * (aux_s + 1)
    warping(ar, aux, start, end, aux_s, wp)
    return ar

