{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_scalar_time_microsecond_Haskell_dict_format_record where
data Val0 = Val0 { exact_millisecond :: String, sub_millisecond :: String }
my_data :: Val0
my_data = Val0 {
    exact_millisecond = "09:30:15.123000",
    sub_millisecond = "09:30:15.123456"
}
main :: IO ()
main = seq my_data (return ())
