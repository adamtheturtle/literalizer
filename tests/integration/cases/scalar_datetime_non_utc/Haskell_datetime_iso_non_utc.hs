{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val =
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = "2024-01-15T18:00:00+05:30"
