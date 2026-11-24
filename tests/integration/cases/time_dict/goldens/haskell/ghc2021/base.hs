module Fixture_time_dict_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("morning", HStr "09:30:00"),
    ("afternoon", HStr "14:15:00"),
    ("evening", HStr "23:59:59")
    ]
main :: IO ()
main = seq my_data (return ())
