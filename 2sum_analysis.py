nums = [1, 3, 6, 5]
target = 8

# find two numbers such that their sum == target

# - we need to read every number in the array -> O(N)

# naive solution
# - find all pairs
# - check if sum == target
for index1 in range(len(nums)):
    for index2 in range(index1+1, len(nums)):
        if nums[index1] + nums[index2] == target:
            print(index1, index2)
            break

# O(N^2)

# improve upon it
# - find two numbers that sum to a target
# - we know the target
# - it's possible to eliminate some pairs without checking their sum
# - if the target is 8 and num = 6,
#   then we dont need to check any other number that is > 2

# log is the opposite of exponent
# + -, * /, ^ log  -> 2^3 = 8, log2(8) = 3
# 10^6 is 1_000_000, log10(1_000_000) = 6

# log10(10) = 10s        # because 10^1 = 10
# log10(100) = 20s       # because 10^2 = 100
# log10(100000000) = 80s  # because 10^2 = 100

# fib(20) -> 1s         # O(2^n)
# fib(30) -> more than a day

# O(1), O(log N), O(N), O(N log N), O(N^2), O(N^3), ..., O(2^N), O(3^N), ... O(N!), O(N^N)


# 10^2 is 100
# 20^2 is 400
# 30^2 is 900
# 40^2 is 1600
# 100^2 is 10000

# 2^10 is 1000
# 2^20 is 1000000
# 2^30 is 1000000000
# 2^40 is 1000000000000
# 2^100 is 1000000000000000000000000000000
#   2*2*2*2*2... 100

# 2! = 2
# 10! 362800
# 70! 10000000000000000000000000000000000000000000000000000000000000000000000000000
#     2*3*4*5*6*7...*100


def binary_search(nums, target):
    start, end = 0, len(nums) - 1
    while start <= end:
        mid = (start + end) // 2

        if nums[mid] == target:
            return mid

        elif nums[mid] < target:
            start = mid+1

        else:
            end = mid-1

    return -1


sorted_nums = sorted(nums)  # N log N

for index1, num in enumerate(sorted_nums):  # N
    index2 = binary_search(nums, target-num)  # log N
    if index2 != -1:
        print(index1, index2, 'of the sorted list')
        break

###################################################


d = {num: index for index, num in enumerate(nums)}  # N

for index1, num in enumerate(nums):  # N
    if target-num in d:              # 1
        index2 = d[target-num]       # 1
        print(index1, index2)
        break

# O(N), O(N)
# O(N log N), O(1)
