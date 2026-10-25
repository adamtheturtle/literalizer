module Fixture_multiline_raw_string_delimiter_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "custom base after empty collision: )\"\nvalue",
    HStr "custom suffix after base collision: )\" and )x0\"\nvalue",
    HStr "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
    HStr "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"
    ]
main :: IO ()
main = seq my_data (return ())
