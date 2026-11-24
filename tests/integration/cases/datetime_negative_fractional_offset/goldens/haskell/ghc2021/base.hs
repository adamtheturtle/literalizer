module Fixture_datetime_negative_fractional_offset_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HDatetime UTCTime
my_data :: Val
my_data = HDatetime (UTCTime (fromGregorian 2000 1 1) (secondsToDiffTime 19800))
main :: IO ()
main = seq my_data (return ())
