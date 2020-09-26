class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def create_linked_list(values):
    ll = Node(values[0])
    last_node = ll
    for v in values[1:]:
        last_node.next = Node(v)
        last_node = last_node.next
    return ll


def print_linked_list(ll):
    node = ll
    while (node is not None):
        print(node.val, end=' -> ')
        node = node.next
    print(None)


def reverse_linked_list(ll):
    start_node = ll
    prev_node, curr_node = start_node, start_node.next

    while(curr_node is not None):
        temp = curr_node.next
        curr_node.next = prev_node
        prev_node = curr_node
        curr_node = temp
    last_node = prev_node

    start_node.next = None
    return last_node


def main():
    ll = create_linked_list([5, 7, 15, 2])

    print('Created Linked List:')
    print_linked_list(ll)
    print()

    ll = reverse_linked_list(ll)
    print('Reversed Linked List:')
    print_linked_list(ll)


if __name__ == "__main__":
    main()
