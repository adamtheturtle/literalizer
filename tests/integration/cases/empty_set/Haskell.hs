module Fixture_empty_set_haskell where
data Val = HSet [Val]
my_data :: Val
my_data = HSet []
