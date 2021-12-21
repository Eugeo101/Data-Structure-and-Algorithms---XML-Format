def format_xml(self):
    lvl = 0
    result = ""
    elements = self
    for e in elements:
        if e[0] == '<' and e[1] == '/':
            lvl -= 1
            result += (('\n' + ('\t' * lvl)) if result[-1] == '>' else '') + e
        elif e[0] == '<':
            result += ("\n" if lvl > 0 else "") + ('\t' * lvl) + e
            lvl += 1
        else:
            result += e
    # open(f"{self.file_name[0:-3]}formatted.xml").write(result)
    return result
