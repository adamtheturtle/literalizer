module check where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = JDatetime UTCTime
my_data :: Val
my_data = JDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000))
