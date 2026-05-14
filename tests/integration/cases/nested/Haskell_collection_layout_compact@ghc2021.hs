module Fixture_nested_Haskell_collection_layout_compact where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("users", HList [HMap [("name", HStr "Bob"), ("tags", HList [HStr "admin", HStr "user"])], HMap [("name", HStr "Carol"), ("tags", HList [HStr "guest"])]])
    ]
main :: IO ()
main = seq my_data (return ())
