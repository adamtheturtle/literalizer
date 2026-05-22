{-# LANGUAGE QuasiQuotes #-}
module Fixture_ordered_map_Haskell_json_type_aeson_value_ordered_map where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"name": "Alice", "age": 30, "active": true} |]
main :: IO ()
main = seq my_data (return ())
