from XML_tree import Node
from validate import *
from graph import *
# import numpy as np
from numpy import zeros


class XML:
    file_name = ""
    file_data = ""
    isValid = False
    tags = []   # unique tags, used for encoding and decoding
    elements = []   # each element used in encoding, formatting, and toJSON

    def __init__(self, file_name=None):
        self.file_name = file_name
        file = open(file_name, "r").read() #array of strings <users>
        self.file_data = self.trim_spaces(file) #[<users>, <user>, <id>1</id>, ..]
            
    def validate_(self):
        err = ""
        if self.file_name[-4:] == ".enc" or self.file_name[-4:] == ".txt":   # File is encoded
            with open(self.file_name, "r") as file:
                self.file_data = file.read()
            self.validate_encoded()
        elif self.file_name[-4:] == ".xml": # File is XML
            elements, err = validate(self.file_name)
            self.elements = elements
            self.tags = self.get_tags()
        return err

    def fix(self):
        self.format_xml()

    # Not very useful in validating just validating number of opening and closing
    # yet it's important to get tags list
    def validate_encoded(self):
        file_data = self.file_data
        reading_head = True
        tags = []
        element = ""
        levels = 0
        for i in range(len(file_data)):
            if reading_head:
                if file_data[i] == ';':
                    tags.append(element)
                    element = ""
                elif file_data[i] == ':':
                    reading_head = False
                else:
                    element += file_data[i]
            else:
                if file_data[i] == '>':
                    levels += 1
                elif file_data[i] == '<':
                    levels -= 1
        self.tags = tags

    def encode(self):
        """
            Encoded file is made of two parts head and body
            head contains all unique tags separated by ; and terminated with :
            ex : users;user;id;followers;:
            then the body:
                suppose we use the following xml :
                    <users>
                        <user>
                            <id>50</id>
                            <empty></empty>
                            <name>Ahmed</name>
                        <user>
                    </users>

                and head is as follows (not in order of appearance and will explain why):
                    id;name;user;users;empty;:
                    0   1   2   3       4


                then we get an encoding as follows:
                    3>2>0>50<4:2>Ahmed<<<

                    each tag replaced by its number
                    > means we go down one level
                    < means we go up one level (closing tag we then use stack to reconstruct it)
                    : means we are on same level (happens with empty tags only)

                so full encoding of previous xml is :
                    id;name;user;users;empty;:3>2>0>50<4:2>Ahmed<<<

                In old validate (consistency) algorithm i was expecting a perfect tags list
                where least common tags take higher numbers so we get the best efficiency
                but since its no longer used we are using alternative function which will give us
                also good but not best efficiency
                least common tags will still get highest numbers but when u go down u don't always
                get best numbers but this won't be a problem at all and won't differ compared to old
                case until u have xml file with like over 18 different tags which is uncommon
                so I didn't try to remake the old algorithm which is possible but will consume
                an O(n) time
                so I followed the concept of make common case fast
        """
        head, body, last_char = "", "", '>'

        elements = self.elements.copy()
        tags = [tag if tag[0] != '<' else tag[1:-1] for tag in self.tags]

        # First we replace opening with their hex index in tags list which is also
        # it's index in head
        for i in range(len(elements)):  # T(n) = n / k = O(n)
            if elements[i][0] == '<':
                if elements[i][1] != '/':
                    elements[i] = str(hex(tags.index(elements[i][1:-1]))[2:])
                else:
                    elements[i] = elements[i][1:-1]

        # Then we fill the head
        for i in range(len(tags)):  # T(n) = O(c)
            head += tags[i] + ';'

        head += ':'
        body += elements[0]

        # Now we prepare the body
        for i in range(1, len(elements)):  # T(n) = n / k = O(n)
            if elements[i][0] != '/':
                body += (">" if last_char == '>' else "") + elements[i]
                last_char = '>'
            else:
                if elements[i - 1] == elements[i][1:]:
                    body += ':'
                else:
                    body += '<'
                last_char = '<'

        result = head + body

        # with open(f"{self.file_name[0:-3]}enc", "w") as w:
        #     w.write(result)
        return result

    # We just reverse what we did in encoding
    def decode(self):
        element = ""
        tags = [tag if tag[0] != '<' else tag[1:-1] for tag in self.tags]
        file_data = self.file_data
        reading_head = True
        decoded = ""
        stack = []
        for i in range(len(file_data)):
            if reading_head:    # Skip head cuz we already have tags list from validate function
                if file_data[i] == ':':
                    reading_head = False
                else:
                    continue
            else:
                if file_data[i] == '>':     # We have an opening
                    element = tags[int(element, 16)]
                    decoded += f"<{element}>"
                    stack.append(element)
                    element = ""
                elif file_data[i] == '<':   # We have a closing
                    decoded += f"{element}</{stack[-1]}>"
                    stack.pop(-1)
                    element = ""
                elif file_data[i] == ':':   # We have an empty tag
                    element = tags[int(element, 16)]
                    decoded += f"<{element}></{element}>"
                    element = ""
                else:
                    element += file_data[i]

        self.file_data = decoded
        self.scrape_data()
        # with open(f"{self.file_name[0:-4]}_decoded.xml", "w") as w:
        #     w.write(self.format_xml(False))
        return decoded

    def scrape_data(self):  # Used to extract elements array from file
        text = self.file_data
        elements = []
        for i in range(len(text)):
            j = i + 1  # used as an index to get the tag name
            k = i + 1  # used as an index to get the tag value
            temp = ""
            temp2 = ""
            if text[i] == '<':  # an openning tag
                temp += text[i]
                try:
                    while text[j] != '>' and text[j] != '!':  # loop until '>' or " " to get the tag name
                        temp += text[j]  # concatenate the tag name to temp
                        j += 1

                    if text[i] == '>' or text[i] == ' ' or text[j] != '/':  # we reached the end of the tag
                        temp += '>'
                        elements.append(temp)
                        if elements[-1] == "<>":  # check if there were empty tags and remove them
                            elements.pop()
                except:
                    pass
            elif text[i] == ">":  # this part is to get the vlaue of the tag (i.e. <tag>value</tag>)
                if i == len(text) - 1:  # we reached the end of the text
                    break
                while text[k] != '<':
                    if k == len(text) - 1:  # we reached the end of the text
                        break
                    temp2 += text[k]
                    k += 1
                elements.append(temp2)
                if elements[-1] == " " or elements[-1] == '' or elements[-1] == '  ':  # make sure we didn't get empty spaces as elements
                    elements.pop()
        self.elements = elements

    # Get unique tags, needed for encoding
    def get_tags(self):
        result = []
        for element in self.elements:
            if element[0] == "<" and element[1] != "/" and element not in result: #<user> <user> X
                result.append(element)
        result.reverse()
        return result

    # Just formatting
    def format_xml(self, write_to_file=True):
        lvl = 0
        result = ""
        elements = self.elements
        
        for e in elements:
            if e[0] == '<' and e[1] == '/': #</closed>
                lvl -= 1
                result += (('\n' + ('\t' * lvl)) if result[-1] == '>' else '') + e
            elif e[0] == '<': #</opened>
                result += ("\n" if lvl > 0 else "") + ('\t' * lvl) + e
                lvl += 1
            else: #leaf(data)
                result += e
        # if write_to_file:
        #     with open(f"{self.file_name[0:-3]}formatted.xml",'w') as w:
        #         w.write(result)
        return result

    # The main method that will start and end the conversion process
    def to_json(self):
        root = Node.create_xml_tree(self.elements)
        json = "{"
        file_name = self.file_name
        json += self.node_to_json(root)
        json += "\n}"
        # with open(f"{file_name[0:-3]}json", "w") as w:
        #     w.write(json)
        return json

    def graph(self): #big O[n^2]
        '''
        return Adj_Matrix, marker_array
        '''
        root = Node.create_xml_tree(self.elements) #tree made
        num_nodes = len(root.children) #how many users/node
        adj_matrix = zeros((num_nodes, num_nodes)) #make matrix
        id, followers = find_followers_and_id(root) #id and followers
        marker_array = []
        my_list_followers = []
        l = []
        for e in id: #to get leaf nodes for each ID refrence
            printer(e, l) #1
            marker_array.extend(l)
            # print(l)
            l = []
        # print(marker_array)  # [ 1 2 3 ]
        for e in followers: #to get leaf nodes for each followers refrence
            printer(e, l)
            my_list_followers.append(l)
            # print(l)
            l = []
        # print(my_list_followers)  # [ [2, 3] [1] [1] ]
        # now put in adj matrix and map them
        for i in range(len(id)):
            # lets check if he is follower or not
            for elemnto in my_list_followers[i]:
                for j in range(len(marker_array)):
                    if marker_array[j] == elemnto:
                        adj_matrix[i][j] = 1
        return adj_matrix, marker_array
    @staticmethod
    def int_or_str(data=""):    # Used for leaves to check if it's int or str so we add "" to str
        if data.isdigit():
            return int(data)
        return '"{}"'.format(data)

    @staticmethod
    def array_check(node):      # Check if node parent is an array like users and posts
        return node.parent and len(node.parent.children) > 1 and node.parent.children[0].data == node.parent.children[
            1].data

    @staticmethod
    def node_to_json(node):
        lvl = node.get_depth() + 1
        node_level = node
        while node_level.parent:    # We use this to get amount of indentation
            if node_level.parent and XML.array_check(node_level.parent):
                lvl += 1
            node_level = node_level.parent

        # Node is array like user, post, and topic
        # we have 2 cases
        # case 1 : topic is array of leaves
        # case 2 : user and post are arrays of tags

        if XML.array_check(node):
            result = '\n{}"{}": ['.format("\t" * lvl, node.data[1:-1])
            siblings = node.parent.children
            for i in range(len(siblings)):
                sibling_children = siblings[i].children
                if node.children[0].data[0] != '<':     # Case 1
                    coma = "," if i < len(siblings) - 1 else ""
                    result += '\n{}{}{}'.format("\t" * (lvl + 1), XML.int_or_str(siblings[i].children[0].data), coma)
                else:   # Case 2
                    result += "\n{}{{".format("\t" * (lvl + 1))
                    for j in range(len(sibling_children)):
                        result += XML.node_to_json(sibling_children[j])
                        coma = "," if j < len(sibling_children) - 1 else ""
                        result += coma
                    result += "\n{}}}".format("\t" * (lvl + 1))
                    coma = "," if i < len(siblings) - 1 else ""
                    result += coma
            result += '\n{}]'.format("\t" * lvl)
            return result
        # Not array
        # 2 cases also
        # Case 1 : id and name have laves
        # Case 2 : post has many children not similar
        else:
            if node.children[0].data[0] != '<':     # Case 1
                leaf = node.children[0].data
                result = '\n{}"{}": {}'.format("\t" * lvl, node.data[1:-1], XML.int_or_str(leaf))
            else:   # Case 2
                result = '\n{}"{}": {{'.format("\t" * lvl, node.data[1:-1])
                if len(node.children) > 1 and node.children[0].data == node.children[1].data:
                    result += XML.node_to_json(node.children[0])
                    result += '\n{}}}'.format("\t" * lvl)
                else:
                    for i in range(len(node.children)):
                        coma = "," if i < len(node.children) - 1 else ""
                        result += XML.node_to_json(node.children[i])
                        result += coma
                    result += '\n{}}}'.format("\t" * lvl)
            return result

    @staticmethod
    def trim_spaces(text):  # Just a trimmer but i think we discarded it final versions of code
        result = ""
        if text[0] == '<':
            result += '<'
        for i in range(1, len(text)):
            if text[i] == '\t' or text[i] == '\n':
                continue
            elif text[i] == ' ' and (
                    text[i - 1] == '>' or text[i + 1] == '<' or text[i + 1] == ' ' or text[i - 1] == ' '):
                continue
            else:
                result += text[i]
        return result

