module Fixture_nested_empty_map_sibling_Haskell_sequence_tuple where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: (Val, Val)
my_data = (
    HMap [("mapping", HMap [])],
    HMap []
    )
main :: IO ()
main = seq my_data (return ())
