{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HSet [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HSet [
    "2024-01-15",
    "2024-06-01"
    ]
