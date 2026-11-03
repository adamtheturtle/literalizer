{-# LANGUAGE OverloadedStrings #-}
module Fixture_datetime_list_Haskell_string_double_dt_iso where
import Data.String (IsString(fromString))
data Val = HList [Val] | HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "2024-01-15T12:30:00.123456+00:00",
    "2024-06-01T08:00:00+00:00"
    ]
main :: IO ()
main = seq my_data (return ())
