{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "a",  -- note a
    "b"  -- note b
    ]
