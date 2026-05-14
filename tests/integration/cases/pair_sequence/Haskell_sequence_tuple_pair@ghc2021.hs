module Fixture_pair_sequence_Haskell_sequence_tuple_pair where
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: (Val, Val)
my_data = (
    1,
    HStr "hello"
    )
main :: IO ()
main = seq my_data (return ())
