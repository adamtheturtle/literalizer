{-# LANGUAGE OverloadedStrings #-}
module Fixture_binary_Haskell_json_type_aeson_value_binary where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "[\"48656c6c6f\"]"))
main :: IO ()
main = seq my_data (return ())
