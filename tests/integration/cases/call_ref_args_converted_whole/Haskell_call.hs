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
data Val = HList [Val]
process :: Val -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- myVar :: Val
    _ <- myVar = HList [
    _ <-     1,
    _ <-     2,
    _ <-     3
    _ <-     ]
    _ <- process(myVar)
    pure ()
