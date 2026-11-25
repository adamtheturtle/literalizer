module Fixture_fractional_epoch_boundaries_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime, picosecondsToDiffTime)
data Val = HList [Val] | HDatetime UTCTime
my_data :: Val
my_data = HList [
    HDatetime (UTCTime (fromGregorian 1970 1 1) (picosecondsToDiffTime 1000000)),
    HDatetime (UTCTime (fromGregorian 1969 12 31) (picosecondsToDiffTime 86399500000000000)),
    HDatetime (UTCTime (fromGregorian 1970 1 1) (secondsToDiffTime 1))
    ]
main :: IO ()
main = seq my_data (return ())
