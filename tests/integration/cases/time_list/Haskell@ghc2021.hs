module Fixture_time_list_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("times", HList [HStr "09:30:00", HStr "17:45:00", HStr "23:59:59"])
    ]
main :: IO ()
main = seq my_data (return ())
