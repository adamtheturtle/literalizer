module Fixture_json5_raw_line_separators_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("double", HStr "a\x2028\&b"),
    ("single", HStr "c\x2029\&d"),
    ("both", HStr "e\x2028\&f\x2029g"),
    ("continued", HStr "hi"),
    ("escaped backslash", HStr "j\\\x2028k")
    ]
main :: IO ()
main = seq my_data (return ())
