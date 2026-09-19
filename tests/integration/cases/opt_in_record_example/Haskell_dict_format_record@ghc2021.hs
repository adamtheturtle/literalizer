{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_opt_in_record_example_Haskell_dict_format_record where
data Val0 = Val0 { name :: String, active :: Bool, scores :: [Integer] }
my_data :: Val0
my_data = Val0 {
    name = "Ada",
    active = True,
    scores = [
        1,
        2,
        3
        ]
}
main :: IO ()
main = seq my_data (return ())
