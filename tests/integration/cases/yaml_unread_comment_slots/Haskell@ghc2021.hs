module Fixture_yaml_unread_comment_slots_Haskell where
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
    ("flow", HList [
        1,
        -- After the first element.
        2
        ]),
    -- Between the key and its value.
    ("gap", 3),
    -- On the block scalar header.
    ("block", HStr "Text.\n"),
    ("anchored", 4),
    ("alias", 4)
    -- On the alias.
    ]
main :: IO ()
main = seq my_data (return ())
