{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
instance IsString Val where
    fromString = HStr
x :: Val
x = HList [
    -- first
    "a",
    -- second
    "b"
    ]
