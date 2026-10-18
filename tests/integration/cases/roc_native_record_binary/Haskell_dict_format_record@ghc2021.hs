{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_roc_native_record_binary_Haskell_dict_format_record where
data Val0 = Val0 { payload :: String }
my_data :: Val0
my_data = Val0 {
    payload = "48656c6c6f"
}
main :: IO ()
main = seq my_data (return ())
