module Check where
import Prelude ((-))
import Partial.Unsafe (unsafeCrashWith)

data Val
    = PInt Int
    | PList (Array Val)
value :: Val
value = PList [
    PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PInt 1]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
]

verify :: Int -> Val -> Int
verify 0 (PInt 1) = 1
verify depth (PList [child]) = verify (depth - 1) child
verify _ _ = unsafeCrashWith "incorrect deep input shape or value"

checked :: Int
checked = verify 400 value
