{-# LANGUAGE QuasiQuotes #-}
module Fixture_float_special_values_Haskell_json_type_aeson_value_float_specials where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [Infinity, -Infinity, NaN] |]
main :: IO ()
main = seq my_data (return ())
