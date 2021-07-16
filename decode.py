# Decodes a value/string of the format f"{d}00{h}00{i}00{j}"
# to d, h, i, j

# For later

def decode_val(value):
    # We reverse the string in order to be able to split at 00
    # while keeping the last digit of multiples of 10
    v = str(value)[::-1]
    temp = v.split("00")
    
    # After that's done, reverse everything back to return it to the original input
    out = []
    for n in temp:
        out = [n[::-1]] + out
    return out

