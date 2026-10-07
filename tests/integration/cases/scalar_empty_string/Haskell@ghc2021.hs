module Fixture_scalar_empty_string_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr ""
main :: IO ()
main = seq my_data (return ())
