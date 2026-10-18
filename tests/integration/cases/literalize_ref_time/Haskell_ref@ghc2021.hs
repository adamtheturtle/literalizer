module Fixture_literalize_ref_time_Haskell_ref where
data Val = HStr String | HMap [(String, Val)]
myTime :: Val
myTime = HStr "01:02:03"
my_data :: Val
my_data = HMap [
    ("x", myTime)
    ]
main :: IO ()
main = seq my_data (return ())
