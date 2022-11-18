# Question 7 #########################################################
# tokens:
# Start with this tokens

EOI = 0  # end of input
TRUE = 1  # Constant True - True
FALSE = 2  # Constant False - False
AND = 3  # Binary Boolean operator AND
OR = 4  # Binary Boolean operator OR
NOT = 5  # Unary Boolean operator NOT
EQ = 6 # equality operator
VAR = 7 # Boolean Variable \$[a-zA-Z]*
LP = 8 # Left parenthesis - \(
RP = 9 # Right parenthesis - \)
ERR = 10  # Showing Error
# end of Question 7 ##################################################


# Question 8 - Grammar ###############################################

# prog -> VAR tail1 | {True | False} tail2 | LP prog RP | NOT prog
# tail1 -> EQ expr tail1 | {OR | AND} expr tail2 | epsilon 
# tail2 -> {OR | AND} term tail2 | NOT term tail2 | epsilon
# expr -> NOT term tail2 | term tail2 
# term ->  TRUE | FALSE | VAR tail1 | LP expr RP

# end of Question 8 ##################################################

# Question 9 - recursive descent parser ###############################


import sys
debug = True

def show(indent,name,s,spp):
    if debug:
        print(indent+name+'("',end='');
        j = len(s)
        for i in range(spp,j):
            print(s[i],sep="",end="")
        print('")',end='\n')
        return
    else:
        return
#end show

def x(indent,name1,name2):
    if debug:
        print(indent+"returned to "+name1+" from "+name2)
    else:
        return
#end x



def EatWhiteSpace(s,spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp=spp+1
        if spp >= j:
            break
        
    return spp
#end EatWhiteSpace

# prog -> VAR tail1 | {True | False} tail2 | LP prog RP | NOT prog
# function prog ------------------------------------------------------------
def prog(s,spp,indent):
    show(indent,'prog',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == VAR:
        spp = ConsumeToken(s,spp)
        res,spp = tail1(s,spp,indent1)
        x(indent1,"prog","tail1")
        return res,spp
    elif token == TRUE or token == FALSE:
        spp = ConsumeToken(s,spp)
        res,spp = tail2(s,spp,indent1)
        x(indent1,"prog","tail2")
        return res,spp
    elif token == LP:
        spp = ConsumeToken(s,spp)
        res,spp = prog(s,spp,indent1)
        x(indent1,"prog","prog")
        if not res:
            return False,spp
        token,spp = NextToken(s,spp)
        return (token == RP),spp
    elif token == NOT:
        spp = ConsumeToken(s,spp)
        res,spp = prog(s,spp,indent1)
        x(indent1,"prog","prog")
        return res,spp
    else:
        return False,spp
#end prog

# tail1 -> EQ expr tail1 | {OR | AND} expr tail2 | epsilon 
# function tail1 --------------------------------------------------------
def tail1(s,spp,indent):
    show(indent,'tail1',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == EQ:
        spp = ConsumeToken(s,spp)
        res,spp = expr(s,spp,indent1)
        x(indent1,"tail1","expr")
        if not res:
            return False,spp
        res,spp = tail1(s,spp,indent1)
        x(indent1,"tail1","expr")
        return res,spp
    
    elif token == AND or token == OR:
        spp = ConsumeToken(s,spp)
        res,spp = expr(s,spp,indent1)
        x(indent1,"tail1","expr")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"tail1","tail2")
        return res,spp
        
    else:
        return True,spp  #epsilon
#end tail1

# expr -> NOT term tail2 | term tail2 
# function expr --------------------------------------------- 
def expr(s,spp,indent):
    show(indent,'expr',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == NOT:
        spp = ConsumeToken(s,spp)
        res,spp = term(s,spp,indent1)
        x(indent1,"expr","term")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"expr","tail2")
        return res,spp
    else:
        res,spp = term(s,spp,indent1)
        x(indent1,"expr","term")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"expr","tail2")
        return res,spp
#end expr

# tail2 -> {AND | OR} term tail2 | NOT term tail2 | epsilon
# function tail2 --------------------------------------------- 
def tail2(s,spp,indent):
    show(indent,'tail2',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == AND or token == OR:
        spp = ConsumeToken(s,spp)
        res,spp = term(s,spp,indent1)
        x(indent1,"tail2","term")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"tail2","tail2")
        return res,spp
    
    elif token == NOT:
        spp = ConsumeToken(s,spp)
        res,spp = term(s,spp,indent1)
        x(indent1,"tail2","term")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"tail2","tail2")
        return res,spp
    
    else:
        return True,spp  #epsilon
#end tail2

# term ->  TRUE | FALSE | VAR tail1 | LP expr RP
# function term --------------------------------------------- 
def term(s,spp,indent):
    show(indent,'term',s,spp)
    indent1 = indent+' '

    token,spp = NextToken(s,spp)
    if token == LP:
        res,spp = expr(s,spp,indent1)
        x(indent1,"term","expr")
        if not res:
            return False,spp
        token,spp = NextToken(s,spp);
        return (token == RP),spp
    elif token == VAR:
        res,spp = tail1(s,spp,indent1)
        x(indent1,"term","tail1")
        return res,spp
    elif token == TRUE or token == FALSE:
        return True,spp
    else:
        return False,spp
    
#end term

# function LookAhead ------------------------------------------- 
def LookAhead(s,spp):
    j = len(s)
    i = spp
    if i >= j:
        return EOI
    while s[i]==" " or s[i]=="\n":
        i = i+1
        if i >= j:
            return EOI

    if s[i] == '=':
        return EQ
    elif s[i] == "T":
        return TRUE
    elif s[i] == "F":
        return FALSE
    elif s[i] == "n":
        return NOT
    elif s[i] == "o":
        return OR
    elif s[i] == "a":
        return AND
    elif s[i] == "$":
        return VAR
    elif s[i] == "(":
        return LP
    elif s[i] == ")":
        return RP
    else:
        return ERR
#end LookAhead



# function NextToken --------------------------------------------- 
def NextToken(s,spp):
    spp1 = spp
    spp = EatWhiteSpace(s,spp)
    j = len(s)
    if spp >= j:
        return ERR,spp1

    if spp >= j:
        return EOI,spp
    elif s[spp] == '=':
        return EQ,spp+1
    if s[spp] == "T":
        return TRUE,spp+4
    if s[spp] == "F":
        return FALSE,spp+5
    if s[spp] == "n":
        return NOT,spp+3
    if s[spp] == "o":
        return OR,spp+2
    if s[spp] == "a":
        return OR,spp+3
    elif s[spp] == "(":
        return LP,spp+1
    elif s[spp] == ")":
        return RP,spp+1
    elif s[spp] == "$":
        counter = 1
        while (spp + counter) < j:
            char = s[spp + counter]
            if (ord(char) >= ord('A') and ord(char) <= ord('Z')) or (ord(char) >= ord('a') and ord(char) <= ord('z')):
                counter += 1
            else:
                break
        return VAR,spp+counter
    else:
        return ERR,spp1
#end NUM

def ConsumeToken(s,spp):
    token,spp = NextToken(s,spp)
    return spp
#end ConsumeToken

#main section
s = "not $A and $B and $C"
res,spp = prog(s,0,"")
print(spp)

# is there a leftover ?
if spp <= len(s)-1:
    print("parse Error")
else:
    if res:
        print("parsing OK")
    else:
        print("parse Error")
#end main section

# end of Question 9 ##################################################