module Fixture_reserved_map_labels_Haskell where
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
    ("if", 1),
    ("then", 2),
    ("else", 3),
    ("let", 4),
    ("in", 5),
    ("using", 6),
    ("missing", 7),
    ("assert", 8),
    ("as", 9),
    ("Infinity", 10),
    ("NaN", 11),
    ("merge", 12),
    ("Some", 13),
    ("toMap", 14),
    ("forall", 15),
    ("with", 16),
    ("ordinary", 17)
    ]
main :: IO ()
main = seq my_data (return ())
