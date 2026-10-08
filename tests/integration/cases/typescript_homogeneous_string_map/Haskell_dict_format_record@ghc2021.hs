{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_typescript_homogeneous_string_map_Haskell_dict_format_record where
data Val0 = Val0 { a :: String, b :: String }
my_data :: Val0
my_data = Val0 {
    a = "x",
    b = "y"
}
main :: IO ()
main = seq my_data (return ())
