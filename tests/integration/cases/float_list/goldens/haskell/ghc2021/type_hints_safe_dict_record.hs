{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_float_list_Haskell_type_hints_safe_dict_record where

my_data :: [Double]
my_data = [
    1.1,
    -2.2,
    3.3
    ]
main :: IO ()
main = seq my_data (return ())
