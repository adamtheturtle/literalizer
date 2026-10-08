{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_opt_in_record_temporal_Haskell_dict_format_record where
import Data.Time
data Val0 = Val0 { event_date :: Day, event_time :: String, event_datetime :: UTCTime }
my_data :: Val0
my_data = Val0 {
    event_date = fromGregorian 2024 1 15,
    event_time = "12:30:00",
    event_datetime = UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000)
}
main :: IO ()
main = seq my_data (return ())
