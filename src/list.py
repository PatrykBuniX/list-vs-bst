class Node:
    def __init__(self, data=None):
        self.value = data
        self.next = None


def __insert_node(head, data):
    new_node = Node(data)

    if head is None:
        head = new_node
    else:
        if head.value > data:
            new_node.next = head
            head = new_node
        else:
            tmp = head
            while tmp.next is not None and tmp.next.value < data:
                tmp = tmp.next
            new_node.next = tmp.next
            tmp.next = new_node

    return head


def construct_node_list(arr):
    head = None
    for i in range(len(arr)):
        head = __insert_node(head, arr[i])
    return head


def find_node(head, item):
    ptr = head
    while ptr:
        if ptr.value == item:
            break
        ptr = ptr.next
    return ptr


def remove_node(node, item):
    while node and node.next:
        next_node = node.next
        if item == next_node.value:
            node.next = next_node.next
            return next_node
        node = node.next
    return None
