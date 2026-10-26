module Fixture_nested_maps_with_opposed_value_types_Haskell where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HList [
    HMap [("input", HMap [("name", HStr "alice"), ("city", HStr "paris")]), ("expected", HMap [("count", 1), ("total", 2)])],
    HMap [("input", HMap [("name", 10), ("city", 20)]), ("expected", HMap [("count", HStr "done"), ("total", HStr "pending")])]
    ]
main :: IO ()
main = seq my_data (return ())
