module Fixture_literalize_ref_deep_nesting_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
deep :: Val
deep = HList [
    HList [
        1,
        2
        ],
    HList [
        3,
        4
        ]
    ]
my_data :: Val
my_data = HMap [
    ("a", HMap [
        ("b", HMap [
            ("c", deep)
            ])
        ])
    ]
main :: IO ()
main = seq my_data (return ())
