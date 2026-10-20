module Fixture_default_helper_name_allocator_Haskell where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
allocator :: Val
allocator = HMap [
    ("a", 1)
    ]
main :: IO ()
main = seq allocator (return ())
