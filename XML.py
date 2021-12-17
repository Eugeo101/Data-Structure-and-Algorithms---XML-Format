from XML_tree import *


class XML:
    file_name = ""
    file_data = ""
    isValid = False
    tags = []   # unique tags, used for encoding and decoding
    elements = []   # each element used in encoding, formatting, and toJSON

    def __init__(self, file_name=None):
        if file_name:
            self.file_name = file_name
            file = open(file_name, "r").read()
            self.file_data = self.trim_spaces(file)
            if file_name[-8:] == ".min.xml":
                self.validate_encoded()
            elif file_name[-4:] == ".xml":
                self.validate()

    def validate(self):
        self.isValid = True

    def validate_encoded(self):
        file_data = self.file_data
        reading_head = True
        tags = []
        element = ""
        levels = 0
        for i in range(len(file_data)):
            if reading_head:
                if file_data[i] == ';':
                    tags += element
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

        if levels == 0:
            self.isValid = True
            self.tags = tags

    def encode(self):
        if not self.isValid:
            raise Exception("File is invalid!")
        head, body, last_char = "", "", '>'

        if len(self.elements) == 0:
            self.scrape_data()

        elements = self.elements
        tags = self.tags

        for i in range(len(elements)):  # T(n) = n / k = O(n)
            if elements[i][0] == '<':
                if elements[i][1] != '/':
                    elements[i] = str(hex(tags.index(elements[i][1:-1]))[2:]) + '$'
                else:
                    elements[i] = elements[i][1:-1]

        for i in range(len(tags)):  # T(n) = O(c)
            head += tags[i] + ';'

        head += ':'
        body += elements[0]
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

        encoded_file_name = self.file_name[0:-3] + "exml"
        f = open(encoded_file_name, "w")
        f.write(head + body)
        f.close()

    def decode(self):
        if not self.isValid:
            raise Exception("File is invalid!")

        element = ""
        tags = self.tags
        file_data = self.file_data
        reading_head = True
        decoded = ""
        stack = []
        for i in range(len(file_data)):
            if reading_head:
                if file_data[i] == ':':
                    reading_head = False
                else:
                    continue
            else:
                if file_data[i] == '>':
                    element = tags[int(element[0:-1], 16)]
                    decoded += f"<{element}>"
                    stack.append(element)
                    element = ""
                elif file_data[i] == '<':
                    decoded += f"{element}</{stack[-1]}>"
                    stack.pop(-1)
                    element = ""
                elif file_data[i] == ':':
                    decoded += f"</{stack[-1]}>"
                    stack.pop(-1)
                    element = ""
                else:
                    element += file_data[i]

        decoded_file_name = self.file_name[0:-4] + "xml"
        f = open(decoded_file_name, "w")
        f.write(self.prettify_data(decoded))
        f.close()

    def scrape_data(self):
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

    def prettify_data(self):
        '''
        Takes the list of tages that was outputted by scrape_data(), reorganizes it, then displays it in a proper order
        '''
        elements = self.elements
        powers = []  # each tag in tags will have a corrosponding power that descripes its location in the hierarchical tree
        level = -1  # start at -1 so that the root would be level 0
        new_text = ""  # contains the new layout of the XML document
        for element in elements:
            if element[0] == "<" and element[1] != "/":
                level += 1
                powers.append(level)
            elif element[0] == "<" and element[1] == "/":
                powers.append(level)
                level -= 1
            else:
                level += 1
                powers.append(level)
                level -= 1

        for i in range(len(elements)):
            indentation = ' ' * 4 * powers[i]
            new_text += indentation + elements[i] + '\n'
        return new_text

    def to_json(self):
        root = Node.create_xml_tree(self.elements)
        json = "{"
        file_name = self.file_name
        json += self.node_to_json(root)
        json += "\n}"
        file = open(file_name[0:-3] + "json", "w")
        file.write(json)

    @staticmethod
    def int_or_str(data=""):
        if data.isdigit():
            return int(data)
        return '"{}"'.format(data)

    @staticmethod
    def array_check(node):
        return node.parent and len(node.parent.children) > 1 and node.parent.children[0].data == node.parent.children[
            1].data


    @staticmethod
    def node_to_json(node):
        lvl = node.get_depth() + 1
        node_level = node
        while node_level.parent:
            if node_level.parent and XML.array_check(node_level.parent):
                lvl += 1
            node_level = node_level.parent
        if XML.array_check(node):
            result = '\n{}"{}": ['.format("\t" * lvl, node.data[1:-1])
            siblings = node.parent.children
            for i in range(len(siblings)):
                sibling_children = siblings[i].children
                if node.children[0].data[0] != '<':
                    coma = "," if i < len(siblings) - 1 else ""
                    result += '\n{}{}{}'.format("\t" * (lvl + 1), XML.int_or_str(siblings[i].children[0].data), coma)
                else:
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
        else:
            if node.children[0].data[0] != '<':
                leaf = node.children[0].data
                result = '\n{}"{}": {}'.format("\t" * lvl, node.data[1:-1], XML.int_or_str(leaf))
            else:
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
    def trim_spaces(text):
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

