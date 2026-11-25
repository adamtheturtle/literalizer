let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let f = \(_ : DVal) -> \(_ : DVal) -> {=}
let _ = f (DVal.DInteger +2) (DVal.DText "hello")  -- trailing note
-- next element
let _ = f (DVal.DInteger +3) (DVal.DText "world")
in {=}
