module Fixture_elm_block_comment_nested_quotes_Haskell_comment_block where
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
    {- { - and { - stay readable -}
    {- balanced { - nested - } and trailing - } stay readable -}
    ("x", 1)
    ]
main :: IO ()
main = seq my_data (return ())
