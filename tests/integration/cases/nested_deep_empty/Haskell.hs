module Fixture_nested_deep_empty_haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [HList [], HList []]
    ]
