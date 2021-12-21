from XML_tree import Node


def node_to_json(node):
    lvl = node.get_depth() + 1
    node_level = node
    while node_level.parent:
        if node_level.parent and array_check(node_level.parent):
            lvl += 1
        node_level = node_level.parent
    if array_check(node):
        result = '\n{}"{}": ['.format("\t" * lvl, node.data[1:-1])
        siblings = node.parent.children
        for i in range(len(siblings)):
            sibling_children = siblings[i].children
            if node.children[0].data[0] != '<':
                coma = "," if i < len(siblings) - 1 else ""
                result += '\n{}{}{}'.format("\t" * (lvl + 1), int_or_str(siblings[i].children[0].data), coma)
            else:
                result += "\n{}{{".format("\t" * (lvl + 1))
                for j in range(len(sibling_children)):
                    result += node_to_json(sibling_children[j])
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
            result = '\n{}"{}": {}'.format("\t" * lvl, node.data[1:-1], int_or_str(leaf))
        else:
            result = '\n{}"{}": {{'.format("\t" * lvl, node.data[1:-1])
            if len(node.children) > 1 and node.children[0].data == node.children[1].data:
                result += node_to_json(node.children[0])
                result += '\n{}}}'.format("\t" * lvl)
            else:
                for i in range(len(node.children)):
                    coma = "," if i < len(node.children) - 1 else ""
                    result += node_to_json(node.children[i])
                    result += coma
                result += '\n{}}}'.format("\t" * lvl)
        return result


def array_check(node):
    return node.parent and len(node.parent.children) > 1 and node.parent.children[0].data == node.parent.children[
            1].data


def to_json(self):
    root = Node.create_xml_tree(self.elements)
    json = "{"
    file_name = self.file_name
    json += self.node_to_json(root)
    json += "\n}"
    open(f"{file_name[0:-3]}json", "w").write(json)
    return json


def int_or_str(data=""):
        if data.isdigit():
            return int(data)
        return '"{}"'.format(data)
