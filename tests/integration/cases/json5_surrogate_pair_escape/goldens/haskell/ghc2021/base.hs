module Fixture_json5_surrogate_pair_escape_Haskell where
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
    ("astral", HStr "😀"),
    ("mixed", HStr "a😀b"),
    ("count", 2),
    ("list", HList [HStr "😀", 1]),
    ("nested", HMap [("inner", HStr "😀")])
    ]
main :: IO ()
main = seq my_data (return ())
