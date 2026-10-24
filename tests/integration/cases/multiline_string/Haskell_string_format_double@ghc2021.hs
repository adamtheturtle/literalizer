{-# LANGUAGE OverloadedStrings #-}
module Fixture_multiline_string_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "first line\n  indented\n\nlast line",
    "\nleading newline",
    " \t\nleading whitespace",
    "trailing newline\n",
    "\nleading and trailing\n",
    "quotes: \"\"\" ''' ` and backslash: \\",
    "interpolation: ${value} #{value} #@value #$value $value",
    "backslash before newline: \\\nnext line",
    "trailing spaces  \nnext",
    "C++ empty delimiter collision: )\"\nvalue",
    "C++ first fallback collision: )\" and )x\"\nvalue",
    "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue",
    "Rust delimiter collision: \"#\nvalue",
    "Lua delimiter collision: ]]\nvalue",
    "Swift delimiter collision: \"\"\"#\nvalue",
    "Swift interpolation collision: \\#(value)\nvalue",
    "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    "NUL followed by a digit: \x00\&7",
    "carriage\rreturn"
    ]
main :: IO ()
main = seq my_data (return ())
