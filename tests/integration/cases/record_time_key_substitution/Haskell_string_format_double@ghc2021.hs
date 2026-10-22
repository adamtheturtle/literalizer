{-# LANGUAGE OverloadedStrings #-}
module Fixture_record_time_key_substitution_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HNull | HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("value", HNull)
    ]
main :: IO ()
main = seq my_data (return ())
