{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_float_Haskell_json_type_aeson_value_float where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "3.14"))
main :: IO ()
main = seq my_data (return ())
