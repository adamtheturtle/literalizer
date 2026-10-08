module Fixture_typescript_homogeneous_string_map_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("a", HStr "x"),
    ("b", HStr "y")
    ]
main :: IO ()
main = seq my_data (return ())
