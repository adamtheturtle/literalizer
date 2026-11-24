module Fixture_binary_list_Haskell_sequence_tuple_binary where
data Val = HStr String | HList [Val]
my_data :: (Val)
my_data = (
    HStr "48656c6c6f"
    )
main :: IO ()
main = seq my_data (return ())
