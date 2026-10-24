{-# LANGUAGE OverloadedStrings #-}
module Fixture_root_reference_marker_is_data_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("$ref", "schema.json")
    ]
main :: IO ()
main = seq my_data (return ())
