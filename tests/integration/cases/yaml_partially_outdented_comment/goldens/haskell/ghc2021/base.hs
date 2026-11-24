module Fixture_yaml_partially_outdented_comment_Haskell where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("a", HMap [
        ("b", HList [1]),
        -- Outdented from the sequence, so the inner mapping claims this.
        ("c", 2)
        ]),
    -- Outdented from the inner mapping too, so the root claims this.
    ("d", 3)
    ]
main :: IO ()
main = seq my_data (return ())
