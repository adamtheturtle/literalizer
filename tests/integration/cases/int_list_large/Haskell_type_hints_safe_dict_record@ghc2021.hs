{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_int_list_large_Haskell_type_hints_safe_dict_record where

my_data :: [Integer]
my_data = [
    1000000,
    -1234,
    255,
    -10
    ]
main :: IO ()
main = seq my_data (return ())
