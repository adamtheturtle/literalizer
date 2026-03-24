import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    -- line 1
    -- line 2
    "a"
    ]
