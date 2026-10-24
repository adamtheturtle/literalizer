module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


std :: Val
std = PDict [
    (Tuple "a" (PInt 1))
]
arena :: Val
arena = PDict [
    (Tuple "a" (PInt 1))
]
allocator :: Val
allocator = PDict [
    (Tuple "a" (PInt 1))
]
my_data :: Val
my_data = PList [
    std,
    arena,
    allocator
]
