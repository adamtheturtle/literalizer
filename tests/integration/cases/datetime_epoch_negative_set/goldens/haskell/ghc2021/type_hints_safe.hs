module Fixture_datetime_epoch_negative_set_Haskell_type_hints_safe where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HSet [Val] | HDatetime UTCTime
my_data :: Val
my_data = HSet [
    HDatetime (UTCTime (fromGregorian 1969 12 31) (secondsToDiffTime 86399))
    ]
main :: IO ()
main = seq my_data (return ())
