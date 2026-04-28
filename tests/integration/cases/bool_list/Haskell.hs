module Fixture_bool_list_Haskell where
data Val = HBool Bool | HList [Val]
my_data :: Val
my_data = HList [
    HBool True,
    HBool False,
    HBool True
    ]
