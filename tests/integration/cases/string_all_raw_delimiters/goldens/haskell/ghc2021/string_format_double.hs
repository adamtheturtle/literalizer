{-# LANGUAGE OverloadedStrings #-}
module Fixture_string_all_raw_delimiters_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "x\nx\"###############################################################################################################################################################################################################################################################"
main :: IO ()
main = seq my_data (return ())
