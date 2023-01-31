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
            # Remove the first item(node) from list
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

    def dfs_pre_order(self):
        """
        Data is being put to result before the traversal of a side is completed.\n
        ***First append the value to the results list, then traverse to the left then right(Preorder).\n
        Callstack is heavily used.\n
        :return: results: list
        """
        results = []

        # Create a inner Recursive function
        def traverse(current_node):
            # Append everytime to the current_node(recursively), for left then right (*always) and add to Callstack
            results.append(current_node.value)

            if current_node.left is not None:
                # Append the current_node(recursively - add all elements that are on the left side of the the tree)
                #   for each left node and add to Callstack -> 47, 21, 18
                traverse(current_node.left)
            if current_node.right is not None:
                # Next, Append the current_node(recursively-add all elements that are on the right side of the the tree)
                traverse(current_node.right)

        '''
        For each right node node and add to Callstack -> 47,21,18, [At 18 there is no left or right 
            so out of call stack, next is 21(left is already in the callstack, so moving to the 
            right(empty). Finally moving to 47)] --> [47, 21, 18, 27, 76, 52, 82]
        '''
        # Start the recursion with root_node
        traverse(self.root)
        return results

    def dfs_post_order(self):
        """
        Data is being put to result after the traversal of a side is completed.\n
        ***First traverse to the left then right, then append to the results list.\n
        Callstack is heavily used.\n
        eg: [18, 27, 21, 52, 82, 76, 47]\n
        :return:
        """
        results = []

        # Create a inner Recursive function
        def traverse(current_node):
            if current_node.left is not None:
                # Go through the current_node(recursively - all elements that are on the left side of the the tree)
                traverse(current_node.left)
            if current_node.right is not None:
                # Go through the current_node(recursively - all elements that are on the right side of the the tree)
                traverse(current_node.right)
            # Append to the current_node after arranging, for left then right (*always) and remove from Callstack
            results.append(current_node.value)

        # Start the recursion with root_node
        traverse(self.root)
        return results

    def dfs_in_order(self):
        """
        Data is being put to result after the traversal of a side is completed.\n
        ***Simultaneously traverse and append to the result list. First the left is traversed and added to callstack, then the rig\n
        Callstack is heavily used.\n
        eg: [18, 27, 21, 52, 82, 76, 47]\n
        :return:
        """
        if self.root is None:
            return []
        results = []

        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            results.append(current_node.value)
            if current_node.right is not None:
                traverse(current_node.right)
        traverse(self.root)
        return results


my_tree = BinarySearchTree()
# my_tree.insert(47)
# my_tree.insert(21)
# my_tree.insert(76)
# my_tree.insert(18)
# my_tree.insert(27)
# my_tree.insert(52)
# my_tree.insert(82)

print(my_tree.dfs_in_order())

# [18, 21, 27, 47, 52, 76, 82]
