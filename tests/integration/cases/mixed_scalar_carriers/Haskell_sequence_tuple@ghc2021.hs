module Fixture_mixed_scalar_carriers_Haskell_sequence_tuple where
data Val = HInt Integer | HFloat Double | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: (Val, Val, Val)
my_data = (
    1,
    HStr "a",
    2.5
    )
main :: IO ()
main = seq my_data (return ())
