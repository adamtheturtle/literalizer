class Main {
    public static void main() {
var my_data = new String[]{
    """
first line
  indented

last line""",
    """

leading newline""",
    """
 \t
leading whitespace""",
    """
trailing newline
""",
    """

leading and trailing
""",
    """
quotes: \"\"\" ''' ` and backslash: \\""",
    """
interpolation: ${value} #{value} #@value #$value $value""",
    """
backslash before newline: \\
next line""",
    """
trailing spaces\s\s
next""",
    """
C++ empty delimiter collision: )\"
value""",
    """
C++ first fallback collision: )\" and )x\"
value""",
    """
C++ second fallback collision: )\" and )x\" and )x0\"
value""",
    """
Rust delimiter collision: \"#
value""",
    """
Lua delimiter collision: ]]
value""",
    """
Swift delimiter collision: \"\"\"#
value""",
    """
Swift interpolation collision: \\#(value)
value""",
    """
Ruby fallback interpolation\s\s
#{expression} #@instance #$global""",
    """
NUL followed by a digit: \0007""",
    """
carriage\rreturn"""
};
    }
}
