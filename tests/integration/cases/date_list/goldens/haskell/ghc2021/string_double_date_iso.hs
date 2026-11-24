{-# LANGUAGE OverloadedStrings #-}
module Fixture_date_list_Haskell_string_double_date_iso where
import Data.String (IsString(fromString))
data Val = HList [Val] | HStr String
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "2024-01-15",
    "2024-02-20"
    ]
main :: IO ()
main = seq my_data (return ())
