let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> {=}
let _ = process (DVal.DInteger +1)  -- note<U+2028>still commented<U+2029>done
in {=}
