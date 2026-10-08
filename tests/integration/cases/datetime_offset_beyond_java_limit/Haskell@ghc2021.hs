module Fixture_datetime_offset_beyond_java_limit_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2020 6 14) (secondsToDiffTime 43260))
main :: IO ()
main = seq my_data (return ())
