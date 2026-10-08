{-# LANGUAGE OverloadedStrings #-}
module Fixture_go_bom_string_Haskell_bom_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("x", "\xfeff")
    ]
main :: IO ()
main = seq my_data (return ())
