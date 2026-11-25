{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_float_fixed_small_Haskell_dict_format_record where

my_data :: [Double]
my_data = [
    1.0e-09,
    -1.0e-09
    ]
main :: IO ()
main = seq my_data (return ())
