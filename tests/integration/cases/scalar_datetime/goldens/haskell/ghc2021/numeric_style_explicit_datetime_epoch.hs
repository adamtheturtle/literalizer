module Fixture_scalar_datetime_Haskell_numeric_style_explicit_datetime_epoch where
data Val = HInt Integer
my_data :: Val
my_data = HInt 1705321800
main :: IO ()
main = seq my_data (return ())
