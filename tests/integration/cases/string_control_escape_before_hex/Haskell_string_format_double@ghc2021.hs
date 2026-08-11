{-# LANGUAGE OverloadedStrings #-}
module Fixture_string_control_escape_before_hex_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "a\x07\&face"
main :: IO ()
main = seq my_data (return ())
