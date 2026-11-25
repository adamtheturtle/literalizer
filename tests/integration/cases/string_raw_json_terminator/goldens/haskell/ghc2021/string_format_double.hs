{-# LANGUAGE OverloadedStrings #-}
module Fixture_string_raw_json_terminator_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    (")json", "x")
    ]
main :: IO ()
main = seq my_data (return ())
