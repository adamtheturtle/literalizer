module Fixture_zig_default_helper_name_arena_Haskell where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
arena :: Val
arena = HMap [
    ("a", 1)
    ]
main :: IO ()
main = seq arena (return ())
