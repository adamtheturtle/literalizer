module Check where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (picosecondsToDiffTime 45045123456000000))
