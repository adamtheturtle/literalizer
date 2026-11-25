{-# LANGUAGE OverloadedStrings #-}
module Fixture_empty_key_is_data_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val] | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    HMap [("", "external_value")]
    ]
main :: IO ()
main = seq my_data (return ())
