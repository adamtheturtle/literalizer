{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val] | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    HMap [("first", "Alice"), ("last", "Smith"), ("middle", "Jane")],
    HMap [("first", "Bob"), ("last", "Jones")]
    ]
