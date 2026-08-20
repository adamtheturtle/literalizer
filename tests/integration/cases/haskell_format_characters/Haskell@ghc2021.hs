module Fixture_haskell_format_characters_Haskell where
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
    ("v", HStr "a\xad\x200b\x200d\x200e\x202e\x2060\xfeff\x2028\x2029\&b"),
    ("a\xad\x200b\x200d\x200e\x202e\x2060\xfeff\x2028\x2029\&b", 1)
    ]
main :: IO ()
main = seq my_data (return ())
