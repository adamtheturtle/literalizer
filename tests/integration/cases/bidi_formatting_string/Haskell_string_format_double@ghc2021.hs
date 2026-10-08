{-# LANGUAGE OverloadedStrings #-}
module Fixture_bidi_formatting_string_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("v", "a\x202a\x202b\x202c\x202d\x202e\x2066\x2067\x2068\x2069\&b")
    ]
main :: IO ()
main = seq my_data (return ())
