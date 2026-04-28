module Fixture_mixed_number_list_Haskell_numeric_style_explicit where
data Val = HInt Integer | HFloat Double | HList [Val]
my_data :: Val
my_data = HList [
    HInt 1,
    HFloat (2.5),
    HInt 3
    ]
