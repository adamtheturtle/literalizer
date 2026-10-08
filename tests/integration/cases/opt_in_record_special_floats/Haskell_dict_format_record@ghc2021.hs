{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_opt_in_record_special_floats_Haskell_dict_format_record where
data Val0 = Val0 { positive :: Double, negative :: Double, nan_value :: Double, finite :: Double }
my_data :: Val0
my_data = Val0 {
    positive = (1/0),
    negative = (-1/0),
    nan_value = (0/0),
    finite = 1.5
}
main :: IO ()
main = seq my_data (return ())
