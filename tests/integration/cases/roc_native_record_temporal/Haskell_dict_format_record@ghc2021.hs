{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_roc_native_record_temporal_Haskell_dict_format_record where
import Data.Time
data Val0 = Val0 { birthday :: Day, meeting :: String, event_time :: UTCTime }
my_data :: Val0
my_data = Val0 {
    birthday = fromGregorian 2024 1 15,
    meeting = "09:30:00",
    event_time = UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45000)
}
main :: IO ()
main = seq my_data (return ())
