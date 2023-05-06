from data import generate_random_array


class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None


def __insert(node, value):
    if node is None:
        return Node(value)

    if value < node.value:
        node.left = __insert(node.left, value)
    else:
        node.right = __insert(node.right, value)

    return node


def construct_bst_tree(arr):
    root = None
    for i in range(len(arr)):
        root = __insert(root, arr[i])
    return root


def get_height(root):

    if root is None:
        return 0

    leftChild = get_height(root.left)
    rightChild = get_height(root.right)

    return max(leftChild, rightChild) + 1


def remove_node(root, value):
    if root is None:
        return root

    if value < root.value:
        root.left = remove_node(root.left, value)

    elif (value > root.value):
        root.right = remove_node(root.right, value)

    else:

        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp

        temp = __min_value_node(root.right)
        root.value = temp.value
        root.right = remove_node(root.right, temp.value)

    return root


def __min_value_node(node):
    current = node
    while current.left:
        current = current.left
    return current


def find_node(root, x):
    ptr = root
    while ptr:
        if x > ptr.value:
            ptr = ptr.right
        elif x < ptr.value:
            ptr = ptr.left
        else:
            break
    return ptr


def inorder(root):
    if root is not None:
        inorder(root.left)
        print(root.value, end=' ')
        inorder(root.right)


def postorder(root):
    if root is not None:
        postorder(root.left)
        postorder(root.right)
        print(root.value, end=' ')


def preorder(root):
    if root is not None:
        print(root.value, end=' ')
        preorder(root.left)
        preorder(root.right)


def __get_level_util(node, value, initialLevel):
    if (node == None):
        return 0

    if (node.value == value):
        return initialLevel

    downLevel = __get_level_util(node.left,
                                 value, initialLevel + 1)
    if (downLevel != 0):
        return downLevel

    downLevel = __get_level_util(node.right,
                                 value, initialLevel + 1)
    return downLevel


def get_level(node, value):
    return __get_level_util(node, value, 1)
