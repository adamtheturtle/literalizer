{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_native_record_epoch_Haskell_native_record_epoch where
data Val0 = Val0 { event_time :: Integer }
my_data :: Val0
my_data = Val0 {
    event_time = 1705321800
}
main :: IO ()
main = seq my_data (return ())
