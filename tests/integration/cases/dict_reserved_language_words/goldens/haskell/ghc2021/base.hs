module Fixture_dict_reserved_language_words_Haskell where
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
    ("assert", 1),
    ("else", 1),
    ("error", 1),
    ("false", 1),
    ("for", 1),
    ("function", 1),
    ("if", 1),
    ("import", 1),
    ("importbin", 1),
    ("importstr", 1),
    ("in", 1),
    ("local", 1),
    ("null", 1),
    ("self", 1),
    ("super", 1),
    ("tailstrict", 1),
    ("then", 1),
    ("true", 1),
    ("ordinary", 1)
    ]
main :: IO ()
main = seq my_data (return ())
