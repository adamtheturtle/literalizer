{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("date", "2024-01-15"),
    ("datetime", "2024-01-15T12:30:00+00:00")
    ]
