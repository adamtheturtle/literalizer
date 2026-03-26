{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HStr String | HList [Val] | HMap [(String, Val)]
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    HList [HMap [("name", "Alice")], HMap [("name", "Bob")]],
    HList [HMap [("name", "Charlie")], HMap [("name", "Dave")]]
    ]
