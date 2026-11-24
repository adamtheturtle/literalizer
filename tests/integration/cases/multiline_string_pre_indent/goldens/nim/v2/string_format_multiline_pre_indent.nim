import json
block:
    var my_data = %* "\nfirst line\n  indented\n\nlast line\n"
    doAssert my_data.getStr == "\nfirst line\n  indented\n\nlast line\n"
