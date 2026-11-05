{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_time_list_Haskell_dict_format_record where
data Val0 = Val0 { times :: [String] }
my_data :: Val0
my_data = Val0 {
    times = [
        "09:30:00",
        "17:45:00",
        "23:59:59"
        ]
}
main :: IO ()
main = seq my_data (return ())
