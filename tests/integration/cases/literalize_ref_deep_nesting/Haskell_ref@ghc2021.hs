module Fixture_literalize_ref_deep_nesting_Haskell_ref where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
deep :: Val
deep = HList [
    HList [
        HStr "one",
        HStr "two"
        ],
    HList [
        HStr "three",
        HStr "four"
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
