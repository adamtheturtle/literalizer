module Fixture_literalize_ref_aware_time_Haskell_ref_default where
data Val = HStr String | HMap [(String, Val)]
shared_time :: Val
shared_time = HStr "12:30:15+02:00"
my_data :: Val
my_data = HMap [
    ("x", shared_time)
    ]
main :: IO ()
main = seq my_data (return ())
