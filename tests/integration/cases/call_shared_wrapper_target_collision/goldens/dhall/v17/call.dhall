let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let check = \(_ : DVal) -> {=}
let _ = check (DVal.DInteger +42)
in {=}
