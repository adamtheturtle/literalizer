{-# LANGUAGE OverloadedStrings #-}
module Fixture_noncharacter_string_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("fffe", "\xfffe"),
    ("ffff", "\xffff")
    ]
main :: IO ()
main = seq my_data (return ())
