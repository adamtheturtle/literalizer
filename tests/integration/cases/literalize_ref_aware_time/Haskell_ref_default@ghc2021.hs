module Fixture_literalize_ref_aware_time_Haskell_ref_default where
data Val = HStr String | HMap [(String, Val)]
value :: Val
value = HStr "12:30:15+02:00"
my_data :: Val
my_data = HMap [
    ("x", value)
    ]
main :: IO ()
main = seq my_data (return ())
