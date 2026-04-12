module Check where


data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)


process(PStr "hello")
process(PInt 42)
process(PBool true)
