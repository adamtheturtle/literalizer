module Fixture_bool_list_haskell where
data Val = HBool Bool | HList [Val]
my_data :: Val
my_data = HList [
    HBool True,
    HBool False,
    HBool True
    ]
