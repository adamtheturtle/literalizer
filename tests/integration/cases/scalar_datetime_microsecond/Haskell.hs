module Fixture_scalar_datetime_microsecond_Haskell where
import Data.Time (UTCTime(..), fromGregorian, picosecondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (picosecondsToDiffTime 45000123456000000))
main :: IO ()
main = seq my_data (return ())
