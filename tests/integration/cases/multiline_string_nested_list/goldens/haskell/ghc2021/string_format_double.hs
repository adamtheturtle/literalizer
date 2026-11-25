{-# LANGUAGE OverloadedStrings #-}
module Fixture_multiline_string_nested_list_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    HList ["\nfirst line\n  indented\n\nlast line\n"]
    ]
main :: IO ()
main = seq my_data (return ())
