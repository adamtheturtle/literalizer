module Fixture_negative_zero_constructor_arguments_Haskell_numeric_style_explicit where
data Val = HFloat Double | HList [Val]
my_data :: Val
my_data = HList [
    HFloat (-0.0),
    HFloat (0.0)
    ]
main :: IO ()
main = seq my_data (return ())
