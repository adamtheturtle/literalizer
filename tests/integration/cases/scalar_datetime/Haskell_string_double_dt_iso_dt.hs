{-# LANGUAGE OverloadedStrings #-}
module Fixture_scalar_datetime_Haskell_string_double_dt_iso_dt where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "2024-01-15T12:30:00+00:00"
main :: IO ()
main = seq my_data (return ())
