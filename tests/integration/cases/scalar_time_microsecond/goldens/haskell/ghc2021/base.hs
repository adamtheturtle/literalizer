module Fixture_scalar_time_microsecond_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("exact_millisecond", HStr "09:30:15.123000"),
    ("sub_millisecond", HStr "09:30:15.123456")
    ]
main :: IO ()
main = seq my_data (return ())
