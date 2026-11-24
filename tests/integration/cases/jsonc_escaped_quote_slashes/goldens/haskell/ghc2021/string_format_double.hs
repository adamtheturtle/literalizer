{-# LANGUAGE OverloadedStrings #-}
module Fixture_jsonc_escaped_quote_slashes_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("text", "a\"//b")
    ]
main :: IO ()
main = seq my_data (return ())
