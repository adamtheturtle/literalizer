module Fixture_string_with_backslash_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "C:\\path\\to\\file",
    HStr "back\\\\slash",
    HStr "hello \\\"world\\\"",
    HStr "path\\to \"# file",
    HStr "trailing\\",
    HStr "both \"quotes''' here",
    HStr "line1\\nline2\nwith newline"
    ]
main :: IO ()
main = seq my_data (return ())
