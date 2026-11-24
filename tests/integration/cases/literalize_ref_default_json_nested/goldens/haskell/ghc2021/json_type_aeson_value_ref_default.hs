{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_default_json_nested_Haskell_json_type_aeson_value_ref_default where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
shared :: Value
shared = [aesonQQ| 42 |]
my_data :: Value
my_data = [aesonQQ| {"refs": [#{shared}, #{shared}], "quoted": "#{shared}"} |]
main :: IO ()
main = seq my_data (return ())
