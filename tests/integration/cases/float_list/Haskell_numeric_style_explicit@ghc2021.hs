module Fixture_float_list_Haskell_numeric_style_explicit where
data Val = HFloat Double | HList [Val]
my_data :: Val
my_data = HList [
    HFloat (1.1),
    HFloat (-2.2),
    HFloat (3.3)
    ]
main :: IO ()
main = seq my_data (return ())
