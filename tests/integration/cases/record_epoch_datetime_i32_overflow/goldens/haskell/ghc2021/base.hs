module Fixture_record_epoch_datetime_i32_overflow_Haskell where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HStr String | HMap [(String, Val)] | HDatetime UTCTime
my_data :: Val
my_data = HMap [
    ("within_i32", HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 43200))),
    ("beyond_i32", HDatetime (UTCTime (fromGregorian 2099 6 15) (secondsToDiffTime 30600)))
    ]
main :: IO ()
main = seq my_data (return ())
