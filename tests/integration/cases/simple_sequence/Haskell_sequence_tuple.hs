module Fixture_simple_sequence_Haskell_sequence_tuple where
data Val = HNull | HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: (Val, Val, Val, Val)
my_data = (
    1,
    HStr "hello",
    HBool True,
    HNull
    )
