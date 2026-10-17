module Fixture_yaml_pairs_tag_Haskell where
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
    HMap [("first", 1)],
    HMap [("repeated", HStr "a")],
    HMap [("repeated", HStr "b")]
    ]
main :: IO ()
main = seq my_data (return ())
