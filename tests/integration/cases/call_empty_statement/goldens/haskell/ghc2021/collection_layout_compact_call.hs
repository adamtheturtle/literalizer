module Fixture_call_empty_statement_Haskell_collection_layout_compact_call where
make_widget :: Val -> IO ()
make_widget _ = return ()
data Val = HList [Val]
main :: IO ()
main = do
    _ <- make_widget (HList [])
    pure ()
