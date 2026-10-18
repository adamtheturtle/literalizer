module Fixture_custom_reference_key_is_data_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("reference", HStr "whole")
    ]
main :: IO ()
main = seq my_data (return ())
