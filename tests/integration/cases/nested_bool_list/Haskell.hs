module Fixture_nested_bool_list_Haskell where
data Val = HBool Bool | HList [Val]
my_data :: Val
my_data = HList [
    HList [HBool True, HBool False],
    HList [HBool True, HBool True]
    ]
