{-# LANGUAGE OverloadedStrings #-}
module Fixture_string_escaped_quotes_and_dashes_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "hello \"world\" -- not a comment"
main :: IO ()
main = seq my_data (return ())
