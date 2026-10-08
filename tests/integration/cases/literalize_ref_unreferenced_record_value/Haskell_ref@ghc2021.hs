module Fixture_literalize_ref_unreferenced_record_value_Haskell_ref where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
other :: Val
other = HStr "true"
my_data :: Val
my_data = HMap [
    ("main", HMap [("x", 1), ("y", HStr "s")])
    ]
main :: IO ()
main = seq my_data (return ())
