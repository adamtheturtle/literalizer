{-# LANGUAGE OverloadedStrings #-}
module Fixture_set_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HSet [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HSet [
    "apple",
    "banana",
    "cherry"
    ]
main :: IO ()
main = seq my_data (return ())
