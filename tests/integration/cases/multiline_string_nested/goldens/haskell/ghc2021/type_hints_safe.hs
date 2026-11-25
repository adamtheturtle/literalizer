module Fixture_multiline_string_nested_Haskell_type_hints_safe where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("outer", HList [HList [HStr "nested first line\n  indented\n\nnested last line\n"]])
    ]
main :: IO ()
main = seq my_data (return ())
