{-# LANGUAGE OverloadedStrings #-}
module Fixture_comment_block_scalar_not_comment_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("description", "# not a comment\n"),
    ("name", "foo")
    ]
main :: IO ()
main = seq my_data (return ())
