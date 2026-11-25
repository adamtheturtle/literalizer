module Fixture_scalar_empty_string_Haskell_prefix_J where
data Val = JStr String
my_data :: Val
my_data = JStr ""
main :: IO ()
main = seq my_data (return ())
