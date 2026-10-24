module Fixture_string_with_dollar_Haskell_sequence_tuple where
data Val = HStr String | HList [Val]
my_data :: (Val, Val)
my_data = (
    HStr "price $10",
    HStr "$HOME"
    )
main :: IO ()
main = seq my_data (return ())
