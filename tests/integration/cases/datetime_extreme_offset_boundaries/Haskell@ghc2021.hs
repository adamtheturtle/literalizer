module Fixture_datetime_extreme_offset_boundaries_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HList [Val] | HDatetime UTCTime
my_data :: Val
my_data = HList [
    HDatetime (UTCTime (fromGregorian 2020 6 16) (secondsToDiffTime 43140)),
    HDatetime (UTCTime (fromGregorian 2020 6 16) (secondsToDiffTime 21600)),
    HDatetime (UTCTime (fromGregorian 2020 6 14) (secondsToDiffTime 64800)),
    HDatetime (UTCTime (fromGregorian 2020 6 14) (secondsToDiffTime 43260))
    ]
main :: IO ()
main = seq my_data (return ())
