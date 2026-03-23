{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
instance IsString Val where
    fromString = HStr
import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
x :: Val
x = HMap [
    ("date", HDate (fromGregorian 2024 1 15)),
    ("datetime", HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000)))
    ]
