module Fixture_comments_escaped_single_quote_multiple_Haskell where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
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
    ("host", HStr "it's here"),  -- a comment
    ("port", 80)  -- another
    ]
main :: IO ()
main = seq my_data (return ())
