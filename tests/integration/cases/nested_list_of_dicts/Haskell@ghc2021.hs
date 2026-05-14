module Fixture_nested_list_of_dicts_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HList [HMap [("name", HStr "Alice")], HMap [("name", HStr "Bob")]],
    HList [HMap [("name", HStr "Charlie")], HMap [("name", HStr "Dave")]]
    ]
main :: IO ()
main = seq my_data (return ())
