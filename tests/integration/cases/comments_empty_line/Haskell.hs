{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
import Data.String (IsString(fromString))
instance IsString Val where
    fromString = HStr
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
x :: Val
x = HList [
    "a",
    --
    "b"
    ]
