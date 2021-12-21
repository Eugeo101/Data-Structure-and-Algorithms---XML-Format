from XML_tree import *


# Get closing tag of opening tag
def close_tag(opening: str):
    return "</" + opening[1:]


# Get opening tag of closing tag
def open_tag(closing: str):
    return '<' + closing[2:]


# Check if second word is singular of first for most cases
# like users and user, posts and post, books and book, etc
def is_singular(plural: str, singular: str):
    fixed_plural = ""
    fixed_singular = ""
    for i in range(len(plural)):
        if plural[i].isalpha():
            fixed_plural += plural[i]
    for i in range(len(singular)):
        if singular[i].isalpha():
            fixed_singular += singular[i]

    return fixed_singular == fixed_plural[0:len(fixed_singular)]


# Check if opening exists somewhere before
def found_b4(elements: [str], element: str):
    i = len(elements) - 1
    flag = False
    while i > -1:
        if open_tag(element) == elements[i]:
            if not flag:
                return True
            else:
                flag = False
        elif element == elements[i]:
            flag = True
        i -= 1
    return False


def validate(file_name):
    root = Node("<root>")
    current_node = root
    elements = []
    errors = []
    types = ["Missing opening tag", "Missing closing tag"]
    line_no = 0
    with open(file_name, "r") as file:
        for line in file:
            line_no += 1
            i = 0
            while i < len(line):
                element = ""

                # Trim spaces in the beginning
                while i < len(line) and line[i] == ' ':
                    i += 1
                if i > len(line) - 1:
                    continue

                # Remove declaration tag
                if line[i] == '<' and line[i + 1] in ['?', '!']:
                    while line[i] != '>':
                        i += 1
                    i += 1
                    continue

                # Case 1 | Text before opening means missing closing
                # <user><id>1</id><name>Ahmed<posts> | Tag <name> is missing closing
                # current node = <name>
                if line[i] == '<' and line[i + 1] != '/':
                    while line[i] != '>':
                        element += line[i]
                        i += 1
                    element += '>'
                    if len(elements) > 0 and elements[-1][0] != '<':    # We have a problem
                        elements.append(close_tag(current_node.data))   # Close the unclosed tag
                        error = (line_no, current_node.data, types[1])  # Add error
                        errors.append(error)
                        current_node = current_node.parent  # Back to parent since we closed a tag

                    # Next lines are done after fixing errors or if we are good
                    elements.append(element)  # Add the new tag
                    node = Node(element)
                    current_node.add_child(node)
                    current_node = node  # Set current node to the new tag
                    i += 1
                    continue

                # Case 2 | Text after closing means missing opening
                # <user><id>1</id>Ahmed</name> | Tag <name> is missing opening
                # current node = <user>
                if line[i] != '<':
                    while i < len(line) and line[i] != '<':
                        if line[i] == '\n' or line[i] == '\t':
                            i += 1
                            continue
                        element += line[i]
                        i += 1
                    if not len(element):    # Empty element
                        continue
                    if len(elements) > 0 and len(elements[-1]) > 1 and elements[-1][1] == '/':
                        node = Node("<temp>")   # Temp node to replace </name> opening
                        current_node.add_child(node)    # Place node <temp> under <user> where <name> belongs
                        current_node = node     # Current node is <temp> i.e. <name>
                        elements.append("<temp>")   # Reserve place for <name>
                        elements.append(element)    # Place the text
                        error = line_no   # Place an error with carrying the line no only
                        errors.append(error)
                    else:
                        elements.append(element)
                    continue

                # Case 3 | Closing tag after text missing its opening (finishing case 2 problem)
                # <user><id>1</id>Ahmed</name> | Tag <name> is missing opening
                # current node = <temp>
                if line[i] == '<' and line[i + 1] == '/' and current_node.data == "<temp>":
                    while line[i] != '>':
                        element += line[i]
                        i += 1
                    element += '>'
                    elements[-2] = open_tag(element)    # Replace <temp> with <name>
                    elements.append(element)    # Add the closing tag
                    errors[-1] = (errors[-1], open_tag(element), types[0])  # Fix the error info
                    current_node = current_node.parent
                    i += 1
                    continue

                # Case 4 | Mismatching opening and closing tags
                # 4.1 : <post><topics>finance</post> | Exists above
                # 4.2 : <post>finance</topics></post> | Doesn't exist above
                # current node @4.1, 4.2 = <topics>
                if line[i] == '<' and line[i + 1] == '/':
                    while line[i] != '>':
                        element += line[i]
                        i += 1
                    element += '>'
                    if open_tag(element) != current_node.data:  # We have an error

                        # Case 4.1 the tag is somewhere before
                        if found_b4(elements, element):
                            while current_node.data != open_tag(element):
                                j = len(elements)
                                flag = False
                                while j > - 1:  # Find the opening of previous unclosed tags by going backward
                                    j -= 1
                                    if current_node.data == elements[j]:
                                        # We need to skip opening with their closing as we are looking
                                        # for an opening missing the closing
                                        if flag:
                                            flag = False
                                        else:
                                            break
                                    elif current_node.data == open_tag(elements[j]):
                                        flag = True

                                j += 1
                                lvl = 0
                                is_array = False
                                flag = False
                                while j < len(elements) and lvl > -1:   # Find closing position by going forward
                                    if elements[j][0] == '<' and elements[j][1] == '/':
                                        # Next line can be removed and still get balanced xml but it
                                        # helps get get accurate positions assuming that a tag named posts
                                        # having one child named post is for sure and array of posts
                                        # same for users and user, houses and house, books and book, etc
                                        # we are using a flag to make sure we reach then end of array by skipping
                                        # the child content
                                        if is_array and is_singular(current_node.data, open_tag(elements[j])):
                                            flag = False
                                        lvl -= 1
                                    elif elements[j][0] == '<' and elements[j][1] != '/':
                                        if elements[j] == current_node.data:
                                            break
                                        elif is_singular(current_node.data, elements[j]):
                                            is_array = True
                                            flag = True
                                        elif is_array and not (flag or is_singular(current_node.data, elements[j])):
                                            break
                                        lvl += 1
                                    j += 1
                                elements.insert(j, close_tag(current_node.data))
                                error = (line_no, current_node.data, types[1])
                                errors.append(error)
                                current_node = current_node.parent

                        # Case 4.2 the tag is not found above
                        # Here we will put the opening somewhere before with the correct level
                        else:
                            j = len(elements) - 1
                            lvl = 0
                            is_array = False
                            flag = False
                            # Just as above we can remove is_singular part and still get balanced xml but
                            # I am trying to get accurate positions too
                            # Regarding lvl part we try to get correct position on same level of hierarchy
                            while lvl < 1 and j > -2:
                                if elements[j][0] == '<' and elements[j][1] == '/':
                                    if is_singular(element, elements[j]):
                                        is_array = True
                                        flag = True
                                    elif is_array and not (flag or is_singular(element, elements[j])):
                                        j -= 1
                                        break
                                    lvl -= 1
                                elif elements[j][0] == '<' and elements[j][1] != '/':
                                    if is_array and is_singular(element, elements[j]):
                                        flag = False
                                    lvl += 1
                                j -= 1
                            elements.insert(j + 2, open_tag(element))
                            error = (line_no, element, types[0])
                            errors.append(error)
                            elements.append(element)
                            i += 1
                            continue
                    # Next lines are done after fixing errors or if we are good
                    elements.append(element)
                    current_node = current_node.parent
                    i += 1
                    continue

    # The technique we using up there works from the perspective of closing tag so it
    # will make sure we have closing tags less than or equal
    # opening tags so we need to make sure we close any unclosed tags
    while current_node.data != "<root>":
        error = (line_no, current_node.data, types[1])
        errors.append(error)
        elements.append(close_tag(current_node.data))
        current_node = current_node.parent
    return elements, errors

