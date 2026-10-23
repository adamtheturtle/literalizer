{-# LANGUAGE OverloadedStrings #-}
module Fixture_comment_scalar_quoted_with_hash_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "hello # world"  -- note
main :: IO ()
main = seq my_data (return ())
