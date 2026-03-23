{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "line1\r\nline2",
    "line1\rline2",
    ""
    ]
