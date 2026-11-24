module Fixture_toml_table_string_punctuation_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("comma_hash", HStr "a,#b"),
    ("comma_space_hash", HStr "trail, # comment"),
    ("escaped_quote", HStr "quote \" and , #"),
    ("next_line", HStr "x\x85y"),
    ("line_separator", HStr "x\x2028y"),
    ("paragraph_separator", HStr "x\x2029y")
    ]
main :: IO ()
main = seq my_data (return ())
