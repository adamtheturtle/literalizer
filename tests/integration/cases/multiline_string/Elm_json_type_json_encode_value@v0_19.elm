module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "first line\n  indented\n\nlast line",
    Json.Encode.string "\nleading newline",
    Json.Encode.string " \t\nleading whitespace",
    Json.Encode.string "trailing newline\n",
    Json.Encode.string "\nleading and trailing\n",
    Json.Encode.string "quotes: \"\"\" ''' ` and backslash: \\",
    Json.Encode.string "interpolation: ${value} #{value} #@value #$value $value",
    Json.Encode.string "backslash before newline: \\\nnext line",
    Json.Encode.string "trailing spaces  \nnext",
    Json.Encode.string "C++ empty delimiter collision: )\"\nvalue",
    Json.Encode.string "C++ first fallback collision: )\" and )x\"\nvalue",
    Json.Encode.string "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue",
    Json.Encode.string "Rust delimiter collision: \"#\nvalue",
    Json.Encode.string "Lua delimiter collision: ]]\nvalue",
    Json.Encode.string "Swift delimiter collision: \"\"\"#\nvalue",
    Json.Encode.string "Swift interpolation collision: \\#(value)\nvalue",
    Json.Encode.string "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    Json.Encode.string "NUL followed by a digit: \u{0000}7",
    Json.Encode.string "carriage\rreturn"
    ]
