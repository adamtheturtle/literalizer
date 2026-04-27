module Fixture_empty_dicts_in_sequence_haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [],
    HMap []
    ]
