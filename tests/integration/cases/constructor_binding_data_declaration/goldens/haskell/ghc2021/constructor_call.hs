module Fixture_constructor_binding_data_declaration_Haskell_constructor_call where

data Playlist = Playlist ()
data Val = HList [Val]
main :: IO ()
main = do
    let created = Playlist
    seq created (pure ())
