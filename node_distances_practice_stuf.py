# Given an arbitrary unweighted rooted tree which consists of N nodes.

# The goal of the problem is to find largest distance between two nodes in a tree.

# Distance between two nodes is a number of edges on a path between the nodes (there will be a unique path between any pair of nodes since it is a tree).

# The nodes will be numbered 0 through N - 1.

# The tree is given as an array A, there is an edge between nodes A[i] and i (0 <= i < N). Exactly one of the i's will have A[i] equal to -1, it will be root no
#      5 4
#     /
#    3 3
#   /
#   4 max(2,2) => 2 2 + 2
#   /\
#  5 1 7 1
#  /   \
# 6 0   8 0

# For node in leaves a: n
#   for node b in leaves: n
#     get distance: log n


# i == index -> A[i] == parent

#      0
#   /  |  \
#  1   2   3
#           \
#            4

#  P = [-1, 0, 0, 0, 3]
#  0  1  2  3  4

#      0
#   /    \
#  1      3
#           \
#            4

# for node in nodes: max(node)


class Solution:
    # @param A : list of integers
    # @return an integer

    def solve(self, parents):
        max_edge_count = 0

        for index_a in parents:
            for index_b in parents:
                ancestors = set()
                edge_count = 0
                while index_a != -1:
                    ancestors.add(parents[index_a])
                    index_a = parents[index_a]
                    edge_count += 1

                subtraction_mode = False
                while index_b != -1:
                    if index_b in ancestors:
                        # found common ancestor
                        subtraction_mode = True

                    index_b = parents[index_b]
                    edge_count += -1 if subtraction_mode else 1

                max_edge_count = max(max_edge_count, edge_count)  # 1, 2

            return max_edge_count


# #  P = [-1, 0, 0, 0, 3]

# from collections import defaultdict

# class Solution:
# 	# @param A : list of integers
# 	# @return an integer

# 	def solve(self, parents):
# 	    children = defaultdict(list)
# 	    for index in parents:
# 	        if parents[index] == -1:
# 	            continue

# 	        parent_index = parents[index]
# 	        children[parent_index].append(index)

# 	   # {-1: [0, 1, 2], 0: [3], 3: [4]}
# 	    ans = 0
# 	    for index in parents:
# 	        if node == -1: return 0

#             edge_sums = sum(edges(child) for child in children[node])
#             if edge_sums > ans:
#                 ans = edge_sums

#             return max(edge_sums) + 1

#         return ans
