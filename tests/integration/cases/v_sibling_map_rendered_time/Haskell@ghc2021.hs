module Fixture_v_sibling_map_rendered_time_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("a", HMap [("k", HStr "07:30:00")]),
    ("b", HMap [("k", HStr "string")])
    ]
main :: IO ()
main = seq my_data (return ())
