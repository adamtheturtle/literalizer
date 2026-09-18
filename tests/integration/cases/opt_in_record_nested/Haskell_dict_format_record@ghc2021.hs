{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_opt_in_record_nested_Haskell_dict_format_record where
data Val1 = Val1 { name :: String, active :: Bool }
data Val2 = Val2 { name :: String, score :: Double }
data Val0 = Val0 { owner :: Val1, members :: [Val2] }
my_data :: Val0
my_data = Val0 {
    owner = Val1 {
        name = "Ada",
        active = False
    },
    members = [
        Val2 {
            name = "Ada",
            score = 1.5
        },
        Val2 {
            name = "Bob",
            score = 2.5
        }
        ]
}
main :: IO ()
main = seq my_data (return ())
