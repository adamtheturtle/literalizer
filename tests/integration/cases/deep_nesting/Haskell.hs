module Fixture_deep_nesting_Haskell where
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
    ("level1", HMap [("level2", HMap [("level3", HMap [("level4", HMap [("value", HStr "deep"), ("items", HList [HStr "a", HStr "b"])])]), ("sibling", 42)]), ("tags", HList [HMap [("name", HStr "tag1"), ("meta", HMap [("priority", 1), ("labels", HList [HStr "x", HStr "y"])])]])])
    ]
main :: IO ()
main = seq my_data (return ())
