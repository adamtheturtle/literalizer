module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- A JSONC input case with both comment forms.
    (Tuple "url" (PStr "https://example.org/a/*b*/")),  -- detail
    -- continued
    (Tuple "count" (PInt 0x2))  -- trailing line comment
]
