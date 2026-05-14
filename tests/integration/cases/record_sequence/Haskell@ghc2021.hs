module Fixture_record_sequence_Haskell where
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
    HMap [("id", 1), ("label", HStr "first")],
    HMap [("id", 2), ("label", HStr "second")],
    HMap [("id", 3), ("label", HStr "third")]
    ]
main :: IO ()
main = seq my_data (return ())
