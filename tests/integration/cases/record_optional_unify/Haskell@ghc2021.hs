module Fixture_record_optional_unify_Haskell where
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
    ("items", HList [HMap [("id", 1)], HMap [("id", 2), ("count", 10)], HMap [("id", 3), ("count", 20)]])
    ]
main :: IO ()
main = seq my_data (return ())
