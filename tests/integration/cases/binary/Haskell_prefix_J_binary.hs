module Fixture_binary_Haskell_prefix_J_binary where
data Val = JStr String | JList [Val]
my_data :: Val
my_data = JList [
    JStr "48656c6c6f"
    ]
