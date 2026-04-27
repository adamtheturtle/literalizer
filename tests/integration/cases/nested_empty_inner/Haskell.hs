module Fixture_nested_empty_inner_haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [],
    HList []
    ]
