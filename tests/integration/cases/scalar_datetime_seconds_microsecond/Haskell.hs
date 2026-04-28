module Fixture_scalar_datetime_seconds_microsecond_Haskell where
import Data.Time (UTCTime(..), fromGregorian, picosecondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (picosecondsToDiffTime 45045123456000000))
