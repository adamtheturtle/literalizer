{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val] | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HMap [
    ("users", HList [HMap [("name", "Bob"), ("tags", HList ["admin", "user"])], HMap [("name", "Carol"), ("tags", HList ["guest"])]])
    ]
