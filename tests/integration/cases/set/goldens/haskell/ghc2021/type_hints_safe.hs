module Fixture_set_Haskell_type_hints_safe where
data Val = HStr String | HSet [Val]
my_data :: Val
my_data = HSet [
    HStr "apple",
    HStr "banana",
    HStr "cherry"
    ]
main :: IO ()
main = seq my_data (return ())
