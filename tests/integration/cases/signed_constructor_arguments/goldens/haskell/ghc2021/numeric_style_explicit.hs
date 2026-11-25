module Fixture_signed_constructor_arguments_Haskell_numeric_style_explicit where
data Val = HInt Integer | HFloat Double | HList [Val]
my_data :: Val
my_data = HList [
    HInt (-42),
    HInt 0,
    HInt 42,
    HFloat (-1.25),
    HFloat (0.0),
    HFloat (1.25)
    ]
main :: IO ()
main = seq my_data (return ())
