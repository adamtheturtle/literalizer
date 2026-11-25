module Fixture_del_nel_and_c1_control_strings_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("del", HStr "a\x7f\&b"),
    ("nel", HStr "a\x85\&b"),
    ("c1", HStr "a\x9f\&b")
    ]
main :: IO ()
main = seq my_data (return ())
