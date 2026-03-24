module Check where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime, picosecondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDate Day | HDatetime UTCTime
my_data :: Val
my_data = HList [
    HBool True,
    HBool False,
    HBool True
    ]
