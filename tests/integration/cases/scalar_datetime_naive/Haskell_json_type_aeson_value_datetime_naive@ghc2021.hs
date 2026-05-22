{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_datetime_naive_Haskell_json_type_aeson_value_datetime_naive where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "\"2024-01-15T12:30:00Z\""))
main :: IO ()
main = seq my_data (return ())
