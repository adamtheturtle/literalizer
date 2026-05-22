{-# LANGUAGE OverloadedStrings #-}
module Fixture_dates_Haskell_json_type_aeson_value_dates where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "{\"date\": \"2024-01-15\", \"datetime\": \"2024-01-15T12:30:00+00:00\"}"))
main :: IO ()
main = seq my_data (return ())
