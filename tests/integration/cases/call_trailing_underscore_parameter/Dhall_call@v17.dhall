let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let do_thing = \(_ : DVal) -> {=}
let _ = do_thing (DVal.DInteger +1)
let _ = do_thing (DVal.DInteger +2)
in {=}
