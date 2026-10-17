module Fixture_kotlin_map_of_string_arrays_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("a", HList [HStr "x"]),
    ("b", HList [HStr "y"])
    ]
main :: IO ()
main = seq my_data (return ())
