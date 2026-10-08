{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_elm_native_record_custom_indent_Haskell_native_record_indent_two_spaces where
data Val0 = Val0 { name :: String }
my_data :: Val0
my_data = Val0 {
  name = "Ada"
}
main :: IO ()
main = seq my_data (return ())
