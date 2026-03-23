{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
instance IsString Val where
    fromString = HStr
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
my_data :: Val
my_data = HList [
    "a",
    --
    "b"
    ]
