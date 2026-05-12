module Fixture_empty_list_Haskell_type_hints_safe_seq_tuple where
data Val = HList [Val]
my_data :: ()
my_data = ()
main :: IO ()
main = seq my_data (return ())
