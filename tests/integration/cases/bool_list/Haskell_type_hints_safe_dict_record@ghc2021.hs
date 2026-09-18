{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_bool_list_Haskell_type_hints_safe_dict_record where

my_data :: [Bool]
my_data = [
    True,
    False,
    True
    ]
main :: IO ()
main = seq my_data (return ())
