module Fixture_multiline_sibling_list_widening_Haskell_collection_layout_multiline where
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
    ("omap_value", HMap [
        ("first", 1)
        ]),
    ("sibling_lists", HMap [
        ("numbers", HList [
            1,
            2
            ]),
        ("strings", HList [
            HStr "x",
            HStr "y"
            ])
        ]),
    ("ref_marker_present", HList [
        HStr "$keep",
        HStr "z"
        ])
    ]
main :: IO ()
main = seq my_data (return ())
