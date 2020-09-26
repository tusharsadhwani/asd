"""Python code to Invert a Binary Tree"""

class Node:
    """A tree node. contains a value, and two pointers left and right"""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


    def print_inorder(self):
        """Prints the binary tree using inorder method"""
        if self.left is not None:
            self.left.print_inorder()

        print(self.value, end=' ')

        if self.right is not None:
            self.right.print_inorder()


    def reverse(self):
        """Reverses the tree inplace"""
        self.left, self.right = self.right, self.left

        if self.left is not None:
            self.left.reverse()
        if self.right is not None:
            self.right.reverse()


def main():
    """Main Function"""

    #      5
    #    /   \
    #   2     7
    #  / \   / \
    # 8   1 4   3
    root = Node(
        5,
        Node(
            2,
            Node(8),
            Node(1),
        ),
        Node(
            7,
            Node(4),
            Node(3),
        )
    )

    print('Created Tree:')
    root.print_inorder()
    print()

    root.reverse()
    print('Reversed Tree:')
    root.print_inorder()
    print()

if __name__ == "__main__":
    main()
