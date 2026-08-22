module Fixture_yaml_nested_sequence_between_comments_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HList [
        HMap [("item", HStr "existing")],
        HStr "kept"
        -- This comment trails the first pair.
        ],
    HList [HMap [("item", HStr "next")], HStr "also kept"],
    -- This comment describes the last pair.
    HList [HMap [("item", HStr "last")], HStr "kept too"]
    ]
main :: IO ()
main = seq my_data (return ())
