{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HStr String | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("key\nwith\nnewlines", "value1"),
    ("key\twith\ttabs", "value2"),
    ("", "value3")
    ]
