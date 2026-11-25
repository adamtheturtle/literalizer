{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_toml_extreme_exponent_zero_Haskell_dict_format_record where
data Val0 = Val0 { value :: Double }
my_data :: Val0
my_data = Val0 {
    value = 0.0
}
main :: IO ()
main = seq my_data (return ())
