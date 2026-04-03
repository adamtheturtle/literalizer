module Check where


import Data.Tuple (Tuple(..))
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- Server configuration
    (Tuple "host" PStr "localhost"),  -- default host
    (Tuple "port" PInt 8080),
    -- Enable debug mode
    (Tuple "debug" PBool true)
    ]
