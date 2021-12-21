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
    result = head + body
    open(f"{self.file_name[0:-3]}enc", "w").write(self.format(result))
    return result


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

    open(f"{self.file_name[0:-3]}xml", "w").write(self.format(decoded)).close() # where is the closing of the file
    return self.format(decoded)