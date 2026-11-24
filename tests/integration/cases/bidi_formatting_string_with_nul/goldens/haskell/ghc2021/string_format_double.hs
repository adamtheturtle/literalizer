{-# LANGUAGE OverloadedStrings #-}
module Fixture_bidi_formatting_string_with_nul_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("v", "a\x202a\x00é😀b")
    ]
main :: IO ()
main = seq my_data (return ())
