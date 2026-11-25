module Fixture_datetime_epoch_wide_set_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HSet [Val] | HDatetime UTCTime
my_data :: Val
my_data = HSet [
    HDatetime (UTCTime (fromGregorian 2099 6 15) (secondsToDiffTime 30600))
    ]
main :: IO ()
main = seq my_data (return ())
