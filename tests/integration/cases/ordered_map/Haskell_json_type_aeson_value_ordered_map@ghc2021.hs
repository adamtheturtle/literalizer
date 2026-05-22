{-# LANGUAGE OverloadedStrings #-}
module Fixture_ordered_map_Haskell_json_type_aeson_value_ordered_map where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "{\"name\": \"Alice\", \"age\": 30, \"active\": true}"))
main :: IO ()
main = seq my_data (return ())
