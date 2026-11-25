{-# LANGUAGE QuasiQuotes #-}
module Fixture_leading_zero_string_mapping_key_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"08": "value"} |]
main :: IO ()
main = seq my_data (return ())
