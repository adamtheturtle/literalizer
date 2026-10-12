module Fixture_literalize_ref_rust_repeated_tuple_copy_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
shared :: (Val, Val)
shared = (
    1,
    HStr "x"
    )
my_data :: (Val, Val)
my_data = (
    shared,
    shared
    )
main :: IO ()
main = seq my_data (return ())
