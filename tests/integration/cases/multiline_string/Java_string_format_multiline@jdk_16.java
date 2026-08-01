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
C++ delimiter collision: )LITERALIZER\"
value""",
    """
Rust delimiter collision: \"#
value""",
    """
Lua delimiter collision: ]]
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
