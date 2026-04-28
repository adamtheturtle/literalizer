{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_string_Haskell_string_format_double where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "hello"
