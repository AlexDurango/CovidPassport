import string

def clearString(arg):

    arg = arg.upper().strip()

    for chr in arg:
        if chr in string.whitespace:
            arg = arg.replace(chr,'')
        
        if chr in string.punctuation:
            if chr == '.':
                arg = arg.replace(chr,'')
            else:
                # Si hay un error, envia true
                return (True, None)

    return (False, arg)
