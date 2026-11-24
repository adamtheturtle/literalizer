{-# LANGUAGE OverloadedStrings #-}
module Fixture_comments_escaped_single_quote_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("key", "it's here")  -- a comment
    ]
main :: IO ()
main = seq my_data (return ())
