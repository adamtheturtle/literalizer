module Fixture_scalar_string_Haskell_type_hints_safe where
data Val = HStr String
my_data :: Val
my_data = HStr "hello"
main :: IO ()
main = seq my_data (return ())
