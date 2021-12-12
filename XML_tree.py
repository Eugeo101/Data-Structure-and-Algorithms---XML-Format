class Node:
    '''
    implenting the node class that we will need to create XML_tree
    '''
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        '''
        this function add a new child node to the existing node
        :param child: any datatype
        :return:nothing
        '''
        child.parent = self     # setting up the parent node to the node object calling this function
        self.children.append(child)

    def print_tree_elements(self, level=0):
        '''
        this function is used to print xml tree elements
        :return:
        '''
        print("\t"*level, self.data)
        if len(self.children) > 0:   # to check if the node object has children nodes or not
            for child in self.children:
                child.print_tree_elements(level + 1)

    def get_depth(self):
        '''
        this function measures the depth of a tree from a certain node
        :return: Level(the depth of the tree measured from this point)
        '''
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    @staticmethod
    def create_xml_tree(elements):
        '''
        this function takes xml file in the form of a list and use to create the XML tree
        :param elements:list
        :return: root node
        '''
        root = Node(elements[0])
        current_node = root
        for i in range(1, len(elements)):
            if elements[i][0] == "<" and elements[i][1] != "/":
                child = Node(elements[i])
                current_node.add_child(child)
                current_node = child
            elif elements[i][0] == "<" and elements[i][1] == "/":
                current_node = current_node.parent
            else:
                child = Node(elements[i])
                current_node.add_child(child)
        return root



"""
from XML_tree import *
elements = ['<users>', '<user>', '<id>', '1', '</id>', '<name>', 'Ahmed Ali', '</name>', '<posts>', '<post>', '<body>', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', '</body>', '<topics>', '<topic>', 'economy', '</topic>', '<topic>', 'finance', '</topic>', '</topics>', '</post>', '<post>', '<body>', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', '</body>', '<topics>', '<topic>', 'solar_energy', '</topic>', '</topics>', '</post>', '</posts>', '<followers>', '<follower>', '<id>', '2', '</id>', '</follower>', '<follower>', '<id>', '3', '</id>', '</follower>', '</followers>', '</user>', '<user>', '<id>', '2', '</id>', '<name>', 'Yasser Ahmed', '</name>', '<posts>', '<post>', '<body>', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', '</body>', '<topics>', '<topic>', 'education', '</topic>', '</topics>', '</post>', '</posts>', '<followers>', '<follower>', '<id>', '1', '</id>', '</follower>', '</followers>', '</user>', '<user>', '<id>', '3', '</id>', '<name>', 'Ahmed Magdy', '</name<posts>', '<posts>', '<post>', '<body>', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', '</body>', '<topics>', '<topic>', 'sports', '</topic>', '</topics>', '</post>', '</posts>', '<followers>', '<follower>', '<id>', '1', '</id>', '</follower>', '</followers>', '</user>', '</users>']

root = Node.create_xml_tree(elements)
root.print_tree_elements()
"""