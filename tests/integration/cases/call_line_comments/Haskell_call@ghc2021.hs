module Fixture_call_line_comments_Haskell_call where
data Val = HStr String | HList [Val]
process :: Val -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- process (HStr "Dune")  -- first edition
    _ <- process (HStr "Solaris")
    _ <- process (HStr "Neuromancer")  -- cyberpunk
    pure ()
