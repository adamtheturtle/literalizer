module Fixture_binary_Haskell_type_hints_safe where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "48656c6c6f"
    ]
main :: IO ()
main = seq my_data (return ())
