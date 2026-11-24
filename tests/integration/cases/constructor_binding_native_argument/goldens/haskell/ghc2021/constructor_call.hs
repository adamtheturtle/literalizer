module Fixture_constructor_binding_native_argument_Haskell_constructor_call where

data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data Playlist = Playlist Val
main :: IO ()
main = do
    let created = Playlist (1)
    case created of
        Playlist (HInt 1) -> pure ()
        _ -> error "changed constructor argument"
