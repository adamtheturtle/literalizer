module Check where
import Data.Time (Day, UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
x :: Val
x = HList [
    HDate (fromGregorian 2024 1 15),
    HDate (fromGregorian 2024 2 20)
    ]
