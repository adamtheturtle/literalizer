module Fixture_string_with_dollar_brace_Haskell_sequence_tuple where
data Val = HStr String | HList [Val]
my_data :: (Val, Val)
my_data = (
    HStr "prefix ${HOME} suffix",
    HStr "${interpolated}"
    )
main :: IO ()
main = seq my_data (return ())
