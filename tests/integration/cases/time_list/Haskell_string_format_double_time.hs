{-# LANGUAGE OverloadedStrings #-}
module Fixture_time_list_Haskell_string_format_double_time where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val] | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("times", HList ["09:30:00", "17:45:00", "23:59:59"])
    ]
main :: IO ()
main = seq my_data (return ())
