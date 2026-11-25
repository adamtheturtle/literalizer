module Fixture_empty_map_nested_list_value_Haskell_collection_layout_multiline where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HList [
        HMap [
            ("values", HList [
                HList []
                ])
            ],
        HMap []
        ],
    HList [
        HMap [],
        HMap [
            ("values", HList [
                HList []
                ])
            ]
        ]
    ]
main :: IO ()
main = seq my_data (return ())
