module Fixture_multiline_string_Haskell_type_hints_safe where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "first line\n  indented\n\nlast line",
    HStr "\nleading newline",
    HStr " \t\nleading whitespace",
    HStr "trailing newline\n",
    HStr "\nleading and trailing\n",
    HStr "quotes: \"\"\" ''' ` and backslash: \\",
    HStr "interpolation: ${value} #{value} #@value #$value $value",
    HStr "backslash before newline: \\\nnext line",
    HStr "trailing spaces  \nnext",
    HStr "C++ empty delimiter collision: )\"\nvalue",
    HStr "C++ first fallback collision: )\" and )x\"\nvalue",
    HStr "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue",
    HStr "Rust delimiter collision: \"#\nvalue",
    HStr "Lua delimiter collision: ]]\nvalue",
    HStr "Swift delimiter collision: \"\"\"#\nvalue",
    HStr "Swift interpolation collision: \\#(value)\nvalue",
    HStr "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    HStr "NUL followed by a digit: \x00\&7",
    HStr "carriage\rreturn"
    ]
main :: IO ()
main = seq my_data (return ())
