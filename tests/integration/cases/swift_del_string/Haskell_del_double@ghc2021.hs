{-# LANGUAGE OverloadedStrings #-}
module Fixture_swift_del_string_Haskell_del_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("x", "\x7f")
    ]
main :: IO ()
main = seq my_data (return ())
