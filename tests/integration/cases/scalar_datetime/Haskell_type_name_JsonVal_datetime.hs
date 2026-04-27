module check where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data JsonVal = HDatetime UTCTime
my_data :: JsonVal
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000))
