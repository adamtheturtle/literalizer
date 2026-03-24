{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
import Data.String (IsString(fromString))
instance IsString Val where
    fromString = HStr
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
my_data :: Val
my_data = HList [
    "2024-01-15",
    "2024-02-20"
    ]
