module Fixture_literalize_ref_repeated_null_and_literal_Haskell_ref where
data Val = HNull | HList [Val]
value :: Val
value = HNull
my_data :: Val
my_data = HList [
    value,
    value,
    HNull
    ]
main :: IO ()
main = seq my_data (return ())
