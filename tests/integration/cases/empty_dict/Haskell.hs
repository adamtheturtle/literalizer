module Fixture_empty_dict_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap []
