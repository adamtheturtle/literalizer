module Fixture_yaml_sequence_between_comments_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("item", HStr "existing")],
    -- This comment describes the next item.
    HMap [("item", HStr "next")]
    ]
main :: IO ()
main = seq my_data (return ())
