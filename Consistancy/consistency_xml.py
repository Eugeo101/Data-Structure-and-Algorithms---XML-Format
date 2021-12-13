#Pre-defined stack function , import all function in it
from os import close
from consistancy import fix_closing
from stack import*
#Defining Consistency method

def consistency_check(input_file):

    stackxml = []        #Creating an array to hold in it elements provided by user
    outputxml = []         #Creating an output array to have the elements of xml in consistent format
    errors=dict()
    #Check path provided by user
    #path = path.replace('\\', '\\')    #replacing every \\ with \ , part of xml format
    

    token_No = 0                 #initializing line count to 0 to start from first line of provided file
    for token in input_file: #reading file line by line
        for i in range(len(token)-1):
            if (token[i]=='<'):
                if(token[i+1] != '/' and token[i+1] != '!' and token[i+1] != '?' ):
                    j = i+1
                    tag = ''
                    while((token[j] != " " and token[j] != ">") and (j < len(token)-1)):
                        tag += token[j]
                        j = j+1
                    stackxml.append(tag)
                elif(token[i+1] == '/'):
                    j = i+2
                    tag = ''
                    while(token[j] != '>'):

                        tag += token[j]
                        j = j+1
                    try:
                        if(stackxml.pop() != tag):
                            outputxml.append("error in line "+str(token_No)+" the closing tag '"+str(tag)+"' doesnt match it opening")
                            errors[token_No] = tag
              
                    except IndexError:
                        outputxml.append("error in line "+str(token_No)+" the closing tag '"+str(tag)+"' doesnt have its opening")
                        errors[token_No] = tag
            if(token[i]=='>' and token[i-1]=='/'):
                o=stackxml.pop()

        token_No = token_No + 1

    
    if outputxml == []: # if no errors in file produce an output statement "No errors are found."
        return "No Errors are found.",[-1]
    return outputxml,errors

def op_close_tags_indecies(line):
    op = []
    clse = []
    appnd_op = False
    appnd_cl = False
    for i,c in enumerate(line):
        try:
            if c ==  '<' and line[i+1] != "/":
                appnd_op = True
            elif c ==  '<' and line[i+1] == "/":
                appnd_cl = True
            if c ==">":
                appnd_op = False
            elif c ==">":
                appnd_cl = False
            if appnd_op:
                op.append(i)
            if appnd_cl:
                clse.append(i)
        except:
            pass
    return op,clse
def fix_error(input_file,errors):
    new_file  = []
    for i,line in enumerate(input_file):
        if i in errors:
            line = line.rstrip().lstrip()
            correct_tag = errors[i]
            opening_tag = "<"+correct_tag+">"
            closing_tag = "</"+correct_tag+">"
            o,c = op_close_tags_indecies(line)
            line_mod = list(line)
            for i in c[::-1]:
                line_mod.pop(i)
            for i in o[::-1]:
                line_mod.pop(i)
            line_mod.pop(0)
            line_mod = opening_tag+"".join(line_mod)+closing_tag+"\n"
            print(line_mod)
            new_file.append(line_mod)
        else:
            new_file.append(line)
    with open("test_modifited.txt", "w") as w:
        w.writelines(new_file)
#def fix_error2(input_file,errors)
# Test Case testing
input_file = open("test.txt", "r")      #opening file in read mode

x,errors=consistency_check(input_file)
print(errors)
input_file.close()

input_file = open("test.txt", "r")  
new_file = fix_error(input_file,errors)
input_file.close()
#Time complexity is O(n^3)
