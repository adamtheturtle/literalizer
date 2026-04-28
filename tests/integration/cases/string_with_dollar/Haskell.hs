module Fixture_string_with_dollar_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "price $10",
    HStr "$HOME"
    ]
