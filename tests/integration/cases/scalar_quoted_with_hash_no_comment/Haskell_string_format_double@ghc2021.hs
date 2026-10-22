{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_quoted_with_hash_no_comment_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "hello # world"
main :: IO ()
main = seq my_data (return ())
