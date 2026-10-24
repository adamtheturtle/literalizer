: my_data
+arr
    s\" first line\n  indented\n\nlast line" +str
    s\" \nleading newline" +str
    s\"  \t\nleading whitespace" +str
    s\" trailing newline\n" +str
    s\" \nleading and trailing\n" +str
    s\" quotes: \"\"\" ''' ` and backslash: \\" +str
    s\" interpolation: ${value} #{value} #@value #$value $value" +str
    s\" backslash before newline: \\\nnext line" +str
    s\" trailing spaces  \nnext" +str
    s\" C++ empty delimiter collision: )\"\nvalue" +str
    s\" C++ first fallback collision: )\" and )x\"\nvalue" +str
    s\" C++ second fallback collision: )\" and )x\" and )x0\"\nvalue" +str
    s\" Rust delimiter collision: \"#\nvalue" +str
    s\" Lua delimiter collision: ]]\nvalue" +str
    s\" Swift delimiter collision: \"\"\"#\nvalue" +str
    s\" Swift interpolation collision: \\#(value)\nvalue" +str
    s\" Ruby fallback interpolation  \n#{expression} #@instance #$global" +str
    s\" NUL followed by a digit: \x007" +str
    s\" carriage\rreturn" +str
 -arr
;
