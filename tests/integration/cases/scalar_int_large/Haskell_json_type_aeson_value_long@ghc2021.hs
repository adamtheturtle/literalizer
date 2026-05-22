{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_int_large_Haskell_json_type_aeson_value_long where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "2147483648"))
main :: IO ()
main = seq my_data (return ())
