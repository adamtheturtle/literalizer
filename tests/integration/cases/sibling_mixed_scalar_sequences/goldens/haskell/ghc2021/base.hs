module Fixture_sibling_mixed_scalar_sequences_Haskell where
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
    ("left", HList [1, HStr "one"]),
    ("right", HList [2, HStr "two"])
    ]
main :: IO ()
main = seq my_data (return ())
