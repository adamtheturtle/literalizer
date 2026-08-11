{-# LANGUAGE OverloadedStrings #-}
module Fixture_string_embedded_nul_Haskell_string_embedded_nul_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("x", "\x00"),
    ("y", "\x00\&1")
    ]
main :: IO ()
main = seq my_data (return ())
