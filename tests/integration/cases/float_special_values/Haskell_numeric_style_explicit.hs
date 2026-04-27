module Fixture_float_special_values_haskell_numeric_style_explicit where
data Val = HFloat Double | HList [Val]
my_data :: Val
my_data = HList [
    HFloat ((1/0)),
    HFloat ((-1/0)),
    HFloat ((0/0))
    ]
