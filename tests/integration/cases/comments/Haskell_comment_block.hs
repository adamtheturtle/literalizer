module Fixture_comments_Haskell_comment_block where
data Val = HBool Bool | HInt Integer | HStr String | HMap [(String, Val)]
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
    {- Server configuration -}
    ("host", HStr "localhost"),  {- default host -}
    ("port", 8080),
    {- Enable debug mode -}
    ("debug", HBool True)
    ]
