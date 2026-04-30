module Fixture_null_list_Haskell_sequence_tuple_null where
data Val = HNull | HList [Val]
my_data :: (Val, Val)
my_data = (
    HNull,
    HNull
    )
main :: IO ()
main = seq my_data (return ())
