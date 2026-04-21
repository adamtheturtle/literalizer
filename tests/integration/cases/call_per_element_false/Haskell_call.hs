module Check where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process _ = return ()
main :: IO ()
main = do
    process(1)
    pure ()
