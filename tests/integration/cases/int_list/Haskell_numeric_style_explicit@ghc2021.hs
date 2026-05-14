module Fixture_int_list_Haskell_numeric_style_explicit where
data Val = HInt Integer | HList [Val]
my_data :: Val
my_data = HList [
    HInt 1,
    HInt 2,
    HInt 3
    ]
main :: IO ()
main = seq my_data (return ())
