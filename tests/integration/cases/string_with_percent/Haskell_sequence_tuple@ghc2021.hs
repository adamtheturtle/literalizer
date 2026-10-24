module Fixture_string_with_percent_Haskell_sequence_tuple where
data Val = HStr String | HList [Val]
my_data :: (Val, Val)
my_data = (
    HStr "100% done",
    HStr "%(name) is here"
    )
main :: IO ()
main = seq my_data (return ())
