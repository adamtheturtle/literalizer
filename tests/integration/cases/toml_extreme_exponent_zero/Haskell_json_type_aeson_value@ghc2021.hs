{-# LANGUAGE QuasiQuotes #-}
module Fixture_toml_extreme_exponent_zero_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"value": 0.0} |]
main :: IO ()
main = seq my_data (return ())
