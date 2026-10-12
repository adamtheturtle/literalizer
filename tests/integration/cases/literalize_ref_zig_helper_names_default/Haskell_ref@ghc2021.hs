module Fixture_literalize_ref_zig_helper_names_default_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
std :: Val
std = HMap [
    ("a", 1)
    ]
arena :: Val
arena = HMap [
    ("a", 1)
    ]
allocator :: Val
allocator = HMap [
    ("a", 1)
    ]
my_data :: Val
my_data = HList [
    std,
    arena,
    allocator
    ]
main :: IO ()
main = seq my_data (return ())
