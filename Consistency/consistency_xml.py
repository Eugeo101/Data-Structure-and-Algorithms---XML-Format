text = '''
<?xml version="1.0" encoding="UTF-8"?>
<!-- A random selection of elements from data.xml
     Some IDREFS (refs attribute of element pointer) do not have a corresponding id in this sample-->
<?xml-model href="data.rnc" type="application/relax-ng-compact-syntax"?>
<data version="3.0">
   <synsets source="dict/data.adv" xml:base="data.adv.xml">

      <synset id="r00001740" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">a cappella</word>
         <def>without musical accompaniment</def>
         <example>they performed a cappella</example>
      </synset>
      <synset id="r00261389" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">agonizingly</word>
         <word lex_id="0">excruciatingly</word>
         <word lex_id="0">torturously</word>
         <pointer refs="a01711724" source="3" target="6">Derived from adjective</pointer>
         <pointer refs="a01711724" source="2" target="3">Derived from adjective</pointer>
         <pointer refs="a01711724" source="1" target="1">Derived from adjective</pointer>
         <def>in a very painful manner</def>
         <example>the progress was agonizingly slow</example>
      </synset>
      <synset id="r00423888" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">rallentando</word>
         <pointer refs="n07020895">Domain of synset - TOPIC</pointer>
         <def>slowing down</def>
         <example>this passage should be played rallentando</example>
      </synset>
      <synset id="r00471945" type="r">
         <lex_filenum>02</lex_filenum>
         <word lex_id="0">surpassingly</word>
         <pointer refs="a01676026" source="1" target="5">Derived from adjective</pointer>
         <def>to a surpassing degree</def>
         <example>she was a surpassingly beautiful woman</example>
      </synset>
   </synsets>
</data>
'''

#Pre-defined stack function , import all function in it
from stack import*
#Defining Consistency method
def consistency(path):

    stackxml = []        #Creating an array to hold in it elements provided by user
    outputxml = []         #Creating an output array to have the elements of xml in consistent format

    #Check path provided by user
    #path = path.replace('\\', '\\')    #replacing every \\ with \ , part of xml format
    path = path.encode('unicode_escape')

    input_file = open(path, "r")      #opening file in read mode

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
                    except IndexError:
                        outputxml.append("error in line "+str(token_No)+" the closing tag '"+str(tag)+"' doesnt have its opening")

            if(token[i]=='>' and token[i-1]=='/'):
                o=stackxml.pop()

        token_No = token_No + 1

    #while(len(stackxml) != 0):
    #    print(stackxml[-1])
    #    stackxml.pop()
    input_file.close()
    if outputxml == []: # if no errors in file produce an output statement "No errors are found."
        return "No Errors are found."
    return outputxml
# Test Case testing
#x=consistency("E:\Faculty\Senior - 1\First Term\Data Structures & Algorithims\Project\XML-editor-main\XML-editor-main\test.txt")
#print(x)

#Time complexity is O(n^3)
