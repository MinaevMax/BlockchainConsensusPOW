import os
from copy import copy
from collections import deque

from GOST34112018 import GOST341112


def make_hash(data: bytes):
    return GOST341112(data, digest_size=256).digest()


class Node:
    def __init__(self, data: bytes, level: int = 1):
        self.hash = make_hash(data)
        self.left = None
        self.right = None
        self.parent = None
        self.level = level

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __copy__(self):
        new_node = Node.__new__(Node)
        new_node.__dict__ = self.__dict__.copy()
        return new_node


class MerkleTree:
    def __init__(self, leaves_data: list[bytes]):
        self.root = self.build_tree(leaves_data)

    def build_tree(self, leaves_data: list[bytes]) -> Node | None:
        if len(leaves_data) == 0:
            return None
        q = deque()
        for data in leaves_data:
            q.append(Node(data))

        # Обрабатываем очередь, пока не останется 1 элемент (корень)
        while len(q) > 1:
            left = q.popleft()
            if len(q) == 0 or q[0].level != left.level:
                # Если нечётное количество узлов, дублируем последний
                right = copy(left)
            else:
                right = q.popleft()

            combined = left.hash + right.hash
            parent = Node(combined, level=left.level + 1)
            parent.left = left
            parent.right = right
            left.parent = parent
            right.parent = parent

            q.append(parent)

        return q.popleft()  # Корень дерева

    def get_root_hash(self):
        return self.root.hash

    def print_tree(self, node=None, indent=""):
        if node is None:
            node = self.root
        print(f"{indent}Level {node.level}: {node.hash.hex()}")
        if node.left:
            self.print_tree(node.left, indent + "  ")
        if node.right and node.right != node.left:
            self.print_tree(node.right, indent + "  ")


def build_tree_from_data():
    leaves_data = []
    cur_dir = 'data'
    for file in os.listdir(cur_dir):
        if file.endswith(".sig"):
            with open(os.path.join(cur_dir, file), 'rb') as rf:
                leaves_data.append(rf.read())
    return MerkleTree(leaves_data)


if __name__ == '__main__':
    tree = build_tree_from_data()
    print("\nКорень дерева Меркла:", tree.get_root_hash().hex())
    print("\nСтруктура дерева:")
    tree.print_tree()

    print(tree.root.hash, len(tree.root.hash))
