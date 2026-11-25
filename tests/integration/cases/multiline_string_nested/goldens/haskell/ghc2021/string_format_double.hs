{-# LANGUAGE OverloadedStrings #-}
module Fixture_multiline_string_nested_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val] | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("outer", HList [HList ["nested first line\n  indented\n\nnested last line\n"]])
    ]
main :: IO ()
main = seq my_data (return ())
