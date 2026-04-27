module Fixture_binary_haskell_prefix_j_binary where
data Val = JStr String | JList [Val]
my_data :: Val
my_data = JList [
    JStr "48656c6c6f"
    ]
