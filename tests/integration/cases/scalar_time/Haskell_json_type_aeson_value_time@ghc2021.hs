{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_time_Haskell_json_type_aeson_value_time where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "{\"starts_at\": \"09:30:00\"}"))
main :: IO ()
main = seq my_data (return ())
