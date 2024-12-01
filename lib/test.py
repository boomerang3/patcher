def print_spiral(n):
    spiral = [[0] * n for _ in range(n)]
    
    top, left = 0, 0
    bottom, right = n - 1, n - 1
    
    value = 1
    
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            spiral[top][i] = value
            value += 1
        top += 1
        
        for i in range(top, bottom + 1):
            spiral[i][right] = value
            value += 1
        right -= 1
        
        if top <= bottom:
            for i in range(right, left - 1, -1):
                spiral[bottom][i] = value
                value += 1
            bottom -= 1
        
        if left <= right:
            for i in range(bottom, top - 1, -1):
                spiral[i][left] = value
                value += 1
            left += 1
    
    for row in spiral:
        print(" ".join(f"{x:2}" for x in row))