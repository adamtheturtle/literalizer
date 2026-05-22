{-# LANGUAGE OverloadedStrings #-}
module Fixture_nested_mixed_inner_Haskell_json_type_aeson_value_nested_mixed where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
my_data :: Value
my_data = either error id (eitherDecodeStrict (encodeUtf8 "[[1, \"a\"], [2, \"b\"]]"))
main :: IO ()
main = seq my_data (return ())
