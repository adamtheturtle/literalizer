{-# LANGUAGE OverloadedStrings #-}
module Fixture_unicode_line_separators_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "a\x85\&b\x2028\&c\x2029\&d\r\x2028\&e"
main :: IO ()
main = seq my_data (return ())
