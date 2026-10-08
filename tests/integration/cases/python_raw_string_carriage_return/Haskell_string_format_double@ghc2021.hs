{-# LANGUAGE OverloadedStrings #-}
module Fixture_python_raw_string_carriage_return_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("cr", "a\rb"),
    ("crlf", "a\r\nb"),
    ("lf", "a\nb")
    ]
main :: IO ()
main = seq my_data (return ())
