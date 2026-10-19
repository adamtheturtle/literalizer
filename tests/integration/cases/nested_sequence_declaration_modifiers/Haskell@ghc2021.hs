module Fixture_nested_sequence_declaration_modifiers_Haskell where
data Val = HNull | HBool Bool | HInt Integer | HStr String | HList [Val]
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
    HList [],
    HList [1],
    HList [1, 2],
    HList [1, HStr "x", HBool True, HNull],
    HList [1, 2, 3, 4, 5, 6, 7, 8]
    ]
main :: IO ()
main = seq my_data (return ())
