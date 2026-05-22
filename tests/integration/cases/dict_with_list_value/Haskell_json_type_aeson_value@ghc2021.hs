{-# LANGUAGE OverloadedStrings #-}
module Fixture_dict_with_list_value_Haskell_json_type_aeson_value where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "{\"name\": \"Alice\", \"scores\": [10, 20, 30]}"))
main :: IO ()
main = seq my_data (return ())
