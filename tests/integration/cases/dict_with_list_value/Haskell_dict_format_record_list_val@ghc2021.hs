{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_dict_with_list_value_Haskell_dict_format_record_list_val where
data Val0 = Val0 { name :: String, scores :: [Integer] }
my_data :: Val0
my_data = Val0 {
    name = "Alice",
    scores = [
        10,
        20,
        30
        ]
}
main :: IO ()
main = seq my_data (return ())
