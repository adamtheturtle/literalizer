module Fixture_constructor_binding_algebraic_haskell_Haskell_constructor_call_positional where

data Playlist = Playlist ()
data Val = HList [Val]
main :: IO ()
main = do
    let created = Playlist()
    seq created (pure ())
