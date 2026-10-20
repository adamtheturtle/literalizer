module Fixture_consumer_key_binding_Haskell_type_hints_safe where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
key_binding :: Val
key_binding = HMap [
    ("a", 1)
    ]
main :: IO ()
main = seq key_binding (return ())
