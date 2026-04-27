{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_date_Haskell_string_double_date_iso where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "2024-01-15"
