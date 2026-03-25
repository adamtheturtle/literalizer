{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HList [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "2024-01-15",
    "2024-02-20"
    ]
