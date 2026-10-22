{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_empty_string_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = ""
main :: IO ()
main = seq my_data (return ())
