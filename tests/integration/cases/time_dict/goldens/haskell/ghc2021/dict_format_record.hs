{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_time_dict_Haskell_dict_format_record where
data Val0 = Val0 { morning :: String, afternoon :: String, evening :: String }
my_data :: Val0
my_data = Val0 {
    morning = "09:30:00",
    afternoon = "14:15:00",
    evening = "23:59:59"
}
main :: IO ()
main = seq my_data (return ())
