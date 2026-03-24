{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime, picosecondsToDiffTime)
import Data.String (IsString(fromString))
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
instance IsString Val where
    fromString = HStr
my_data :: Val
my_data = HList [
    "a",  -- note a
    "b"  -- note b
    ]
