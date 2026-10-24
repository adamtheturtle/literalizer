module Check exposing (..)


type Val
    = EFloat Float


std : Val
std = EFloat (0 / 0)
