module Fixture_scalar_time_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("starts_at", HStr "09:30:00")
    ]
main :: IO ()
main = seq my_data (return ())
