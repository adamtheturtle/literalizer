module Check exposing (..)


type Val
    = EBool Bool


refFlag : Val
refFlag = EBool True
my_data : Val
my_data = refFlag
