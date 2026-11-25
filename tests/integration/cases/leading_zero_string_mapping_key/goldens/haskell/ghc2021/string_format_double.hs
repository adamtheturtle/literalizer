{-# LANGUAGE OverloadedStrings #-}
module Fixture_leading_zero_string_mapping_key_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("08", "value")
    ]
main :: IO ()
main = seq my_data (return ())
