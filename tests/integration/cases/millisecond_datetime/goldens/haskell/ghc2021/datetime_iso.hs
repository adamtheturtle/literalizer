module Fixture_millisecond_datetime_Haskell_datetime_iso where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("half", HStr "1979-05-27T07:32:00.500000"),
    ("milli", HStr "1979-05-27T07:32:00.100000"),
    ("max_milli", HStr "1979-05-27T07:32:00.999000"),
    ("whole", HStr "1979-05-27T07:32:00")
    ]
main :: IO ()
main = seq my_data (return ())
