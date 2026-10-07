{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_opt_in_record_binary_Haskell_native_record_bytes_base64 where
data Val0 = Val0 { payload :: String }
my_data :: Val0
my_data = Val0 {
    payload = "YWJj"
}
main :: IO ()
main = seq my_data (return ())
