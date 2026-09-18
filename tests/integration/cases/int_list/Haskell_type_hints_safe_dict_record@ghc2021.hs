{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_int_list_Haskell_type_hints_safe_dict_record where

my_data :: [Integer]
my_data = [
    1,
    2,
    3
    ]
main :: IO ()
main = seq my_data (return ())
