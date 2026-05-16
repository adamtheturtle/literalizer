module Fixture_bool_list_Haskell_type_hints_safe_seq_tuple where
data Val = HBool Bool | HList [Val]
my_data :: (Val, Val, Val)
my_data = (
    HBool True,
    HBool False,
    HBool True
    )
main :: IO ()
main = seq my_data (return ())
