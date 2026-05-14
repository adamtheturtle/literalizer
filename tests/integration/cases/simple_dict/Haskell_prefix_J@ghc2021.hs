module Fixture_simple_dict_Haskell_prefix_J where
data Val = JNull | JBool Bool | JInt Integer | JStr String | JMap [(String, Val)]
instance Num Val where
    fromInteger = JInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (JInt n) = JInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = JMap [
    ("name", JStr "Alice"),
    ("age", 30),
    ("active", JBool True),
    ("score", JNull)
    ]
main :: IO ()
main = seq my_data (return ())
