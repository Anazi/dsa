class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        # Case when the tree is empty
        if self.root is None:
            self.root = new_node
            return True
        temp = self.root
        while True:
            # Case when the value already exists in the tree; return False, as insert is not required
            if new_node.value == temp.value:
                return False
            # When new_node.value < temp.value -> For left side of the tree
            if new_node.value < temp.value:
                # Case when the temp node is the leaf (has no branches)
                if temp.left is None:
                    temp.left = new_node
                    return True
                # Continue the while loop(if temp is not None) or exit(if temp is None), based on the tree
                temp = temp.left
            # When new_node.value > temp.value -> For right side of the tree
            else:
                # Case when the temp node is the leaf (has no branches)
                if temp.right is None:
                    temp.right = new_node
                    return True
                # Continue the while loop(if temp is not None) or exit(if temp is None), based on the tree
                temp = temp.right

    def contains(self, value):
        if self.root is None:
            return False
        temp = self.root
        while temp:
            if value < temp.value:
                temp = temp.left
            elif value > temp.value:
                temp = temp.right
            else:
                return True
        return False
  
    def bfs(self):
        current_node = self.root
        # Using list for queue (using for familiarity, not the best choice)
        queue = []
        results = []
        # Append the "entire" current node(important: the whole node is appended i.e; value, left and right)
        queue.append(current_node)
        # Run the while loop as long as the "queue" is not empty
        while len(queue) > 0:
            # Assign the first item(entire node- value, left and right) of the queue to the current node
            current_node = queue.pop(0)
            # Append the current node's value (current_node.value) to the "results" list
            results.append(current_node.value)
            # Append all the values of the breadth if they exist eg: results will have on 2nd iter [21, 76]
            #   Case 1 - When the smaller values side of the current_node (current_node.left) is not None ->
            #       is not a leaf
            if current_node.left is not None:
                queue.append(current_node.left)
            #   Case 1` - When the bigger values side of the current_node(current_node.right) is not None ->
            #       is not a leaf
            if current_node.right is not None:
                queue.append(current_node.right)
        return results


my_tree = BinarySearchTree()
my_tree.insert(47)
my_tree.insert(21)
my_tree.insert(76)
my_tree.insert(18)
my_tree.insert(27)
my_tree.insert(52)
my_tree.insert(82)

print(my_tree.bfs())

# [47, 21, 76, 18, 27, 52, 82]




                



 