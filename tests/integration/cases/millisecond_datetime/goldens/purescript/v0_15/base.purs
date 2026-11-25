module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "half" (PStr "1979-05-27T07:32:00.500000")),
    (Tuple "milli" (PStr "1979-05-27T07:32:00.100000")),
    (Tuple "max_milli" (PStr "1979-05-27T07:32:00.999000")),
    (Tuple "whole" (PStr "1979-05-27T07:32:00"))
]
