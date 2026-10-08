module Fixture_javascript_naive_datetime_milliseconds_Haskell where
import Data.Time (UTCTime(..), fromGregorian, picosecondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2024 1 15) (picosecondsToDiffTime 45001123000000000))
main :: IO ()
main = seq my_data (return ())
