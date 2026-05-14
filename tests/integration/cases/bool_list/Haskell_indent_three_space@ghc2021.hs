module Fixture_bool_list_Haskell_indent_three_space where
data Val = HBool Bool | HList [Val]
my_data :: Val
my_data = HList [
   HBool True,
   HBool False,
   HBool True
   ]
main :: IO ()
main = seq my_data (return ())
