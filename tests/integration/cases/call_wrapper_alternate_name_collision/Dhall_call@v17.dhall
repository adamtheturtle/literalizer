let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let check_wrapper = \(_ : DVal) -> {=}
let _ = check_wrapper (DVal.DInteger +42)
in {=}
