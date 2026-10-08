{-# LANGUAGE OverloadedStrings #-}
module Fixture_single_quoted_crlf_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("x", "line1\r\nline2")
    ]
main :: IO ()
main = seq my_data (return ())
