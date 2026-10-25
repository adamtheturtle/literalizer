{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_value_type_root_string_Haskell_json_type_aeson_value_ref where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
shared :: Value
shared = [aesonQQ| "value" |]
my_data :: Value
my_data = [aesonQQ| {"$ref": "shared"} |]
main :: IO ()
main = seq my_data (return ())
