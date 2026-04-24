module Check where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: (Val, Val) -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- my_var :: Val
    _ <- my_var = HList [
    _ <-     1,
    _ <-     2,
    _ <-     3
    _ <-     ]
    _ <- my_other :: Val
    _ <- my_other = HList [
    _ <-     4,
    _ <-     5,
    _ <-     6
    _ <-     ]
    _ <- process(my_var, 42)
    _ <- process(my_other, 7)
    pure ()
