{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
instance IsString Val where
    fromString = HStr
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
x :: Val
x = HMap [
    ("users", HList [HMap [("name", "Bob"), ("tags", HList ["admin", "user"])], HMap [("name", "Carol"), ("tags", HList ["guest"])]])
    ]
