import sys


class TreeNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def __insert(root, value):
    if not root:
        return TreeNode(value)
    elif value < root.value:
        root.left = __insert(root.left, value)
    else:
        root.right = __insert(root.right, value)
    root.height = 1 + max(get_height(root.left),
                          get_height(root.right))

    balanceFactor = get_balance(root)
    if balanceFactor > 1:
        if value < root.left.value:
            return rightRotate(root)
        else:
            root.left = leftRotate(root.left)
            return rightRotate(root)
    if balanceFactor < -1:
        if value > root.right.value:
            return leftRotate(root)
        else:
            root.right = rightRotate(root.right)
            return leftRotate(root)
    return root


def remove_node(root, value):
    if not root:
        return root
    elif value < root.value:
        root.left = remove_node(root.left, value)
    elif value > root.value:
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
        root.right = remove_node(root.right,
                                 temp.value)
    if root is None:
        return root

    root.height = 1 + max(get_height(root.left),
                          get_height(root.right))
    balanceFactor = get_balance(root)

    if balanceFactor > 1:
        if get_balance(root.left) >= 0:
            return rightRotate(root)
        else:
            root.left = leftRotate(root.left)
            return rightRotate(root)
    if balanceFactor < -1:
        if get_balance(root.right) <= 0:
            return leftRotate(root)
        else:
            root.right = rightRotate(root.right)
            return leftRotate(root)
    return root


def leftRotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(get_height(z.left),
                       get_height(z.right))
    y.height = 1 + max(get_height(y.left),
                       get_height(y.right))
    return y


def rightRotate(z):
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3
    z.height = 1 + max(get_height(z.left),
                       get_height(z.right))
    y.height = 1 + max(get_height(y.left),
                       get_height(y.right))
    return y


def get_height(root):
    if not root:
        return 0
    return root.height


def get_balance(root):
    if not root:
        return 0
    return get_height(root.left) - get_height(root.right)


def __min_value_node(root):
    if root is None or root.left is None:
        return root
    return __min_value_node(root.left)


def preOrder(root):
    if not root:
        return
    print("{0} ".format(root.value), end="")
    preOrder(root.left)
    preOrder(root.right)
# Print the tree


def printHelper(currPtr, indent, last):
    if currPtr != None:
        sys.stdout.write(indent)
        if last:
            sys.stdout.write("R----")
            indent += "     "
        else:
            sys.stdout.write("L----")
            indent += "|    "
        print(currPtr.value)
        printHelper(currPtr.left, indent, False)
        printHelper(currPtr.right, indent, True)


def construct_avl_tree(nums):
    root = None
    for num in nums:
        root = __insert(root, num)
    return root
