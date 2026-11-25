module Fixture_multiline_string_nested_list_Haskell_type_hints_safe where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HList [HStr "\nfirst line\n  indented\n\nlast line\n"]
    ]
main :: IO ()
main = seq my_data (return ())
