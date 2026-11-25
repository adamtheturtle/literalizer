module Fixture_coercion_uniform_dict_shapes_yaml_Haskell_sequence_tuple where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: (Val, Val)
my_data = (
    HMap [("type", HStr "create"), ("name", HStr "a")],
    HMap [("type", HStr "update"), ("name", HStr "b")]
    )
main :: IO ()
main = seq my_data (return ())
