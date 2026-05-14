module Fixture_time_dict_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("morning", "09:30:00"),
    ("afternoon", "14:15:00"),
    ("evening", "23:59:59")
    ]
main :: IO ()
main = seq my_data (return ())
