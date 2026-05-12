module Fixture_mixed_type_dicts_in_sequence_Haskell_type_hints_safe where
data Val = HBool Bool | HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("type", HStr "create"), ("pr_id", HStr "pr_1"), ("draft", HBool True)],
    HMap [("type", HStr "create"), ("pr_id", HStr "pr_2")]
    ]
main :: IO ()
main = seq my_data (return ())
