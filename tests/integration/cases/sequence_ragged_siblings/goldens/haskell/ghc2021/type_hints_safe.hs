module Fixture_sequence_ragged_siblings_Haskell_type_hints_safe where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HList [HStr "set_task", HStr "web", HStr "lint_web"],
    HList [HStr "merge_pipelines"]
    ]
main :: IO ()
main = seq my_data (return ())
