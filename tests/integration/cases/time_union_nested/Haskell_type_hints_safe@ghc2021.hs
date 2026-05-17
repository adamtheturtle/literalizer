module Fixture_time_union_nested_Haskell_type_hints_safe where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("mixed", HList [HList [HStr "09:30:00"], HList []])
    ]
main :: IO ()
main = seq my_data (return ())
