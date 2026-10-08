{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_native_record_large_integer_Haskell_native_record_multiline where
data Val0 = Val0 { value :: Integer }
my_data :: Val0
my_data = Val0 {
    value = 2147483648
}
main :: IO ()
main = seq my_data (return ())
