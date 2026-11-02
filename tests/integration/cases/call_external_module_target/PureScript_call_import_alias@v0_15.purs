module Check where


import Prelude
import LiteralizerSupport.CallTarget as Module
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = Module.func (PInt 1)
    in
    unit
