{-# LANGUAGE OverloadedStrings #-}
module Fixture_datetime_negative_fractional_offset_Haskell_string_double_dt_iso where
import Data.String (IsString(fromString))
data Val = HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "2000-01-01T00:00:00-05:30"
main :: IO ()
main = seq my_data (return ())
