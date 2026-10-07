{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_native_record_iso_temporal_Haskell_native_record_iso_temporal where
data Val0 = Val0 { birthday :: String, moment :: String, at :: String }
my_data :: Val0
my_data = Val0 {
    birthday = "2024-01-15",
    moment = "2024-01-15T12:30:00+00:00",
    at = "09:30:00"
}
main :: IO ()
main = seq my_data (return ())
