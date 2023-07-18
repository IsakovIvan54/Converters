def check_number(N, M):
    intervals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.1]
    
    for interval in intervals:
        lower_bound = N * interval
        upper_bound = N * (interval + 0.1)
        
        if lower_bound <= M <= upper_bound:
            print(f"The number {M} is in the range {interval*100} to {(interval + 0.1)*100} of {N}")
            break
        else:
            print(f"The number {M} is not in the range {interval*100} to {(interval + 0.1)*100} of {N}")
    
N = int(input("Enter the value of N: "))
M = float(input("Enter the value of M: "))

check_number(N, M)