{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_repeated_value_type_Haskell_json_type_aeson_value_ref where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
shared :: Value
shared = [aesonQQ| 42 |]
my_data :: Value
my_data = [aesonQQ| [{"$ref": "shared"}, {"$ref": "shared"}] |]
main :: IO ()
main = seq my_data (return ())
