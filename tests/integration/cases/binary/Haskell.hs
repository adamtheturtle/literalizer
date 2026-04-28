module Fixture_binary_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "48656c6c6f"
    ]
