{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]
instance IsString Val where
    fromString = HStr
x :: Val
x = HMap [
    ("key\nwith\nnewlines", "value1"),
    ("key\twith\ttabs", "value2"),
    ("", "value3")
    ]
