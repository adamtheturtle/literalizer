module Check where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val] | HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (picosecondsToDiffTime 45000123456000000))
