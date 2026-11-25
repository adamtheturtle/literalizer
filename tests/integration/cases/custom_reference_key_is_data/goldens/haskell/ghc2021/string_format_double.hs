{-# LANGUAGE OverloadedStrings #-}
module Fixture_custom_reference_key_is_data_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("reference", "whole")
    ]
main :: IO ()
main = seq my_data (return ())
