{-# LANGUAGE OverloadedStrings #-}
module Fixture_comment_scalar_before_and_inline_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
-- before
my_data :: Val
my_data = "plain"  -- inline
main :: IO ()
main = seq my_data (return ())
