{-# LANGUAGE OverloadedStrings #-}
module Fixture_multiline_string_scalar_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "\nroot first line\n  indented\n\nroot last line\n"
main :: IO ()
main = seq my_data (return ())
