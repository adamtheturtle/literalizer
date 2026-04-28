module Fixture_int_list_with_zero_Haskell_numeric_style_explicit_zero where
data Val = HInt Integer | HList [Val]
my_data :: Val
my_data = HList [
    HInt 0,
    HInt 1,
    HInt (-1)
    ]
main :: IO ()
main = seq my_data (return ())
