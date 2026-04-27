module Fixture_empty_sequence_haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HList [],
    HMap []
    ]
