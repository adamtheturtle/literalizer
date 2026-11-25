module Fixture_mixed_nested_collection_types_Haskell where
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
my_data = HMap [
    ("lists", HList [HList [1], HList [HStr "x"], HList []]),
    ("maps", HList [HMap [("x", 1)], HMap [("x", HStr "s")]]),
    ("empties", HMap [("a", HList [1]), ("b", HList [])])
    ]
main :: IO ()
main = seq my_data (return ())
