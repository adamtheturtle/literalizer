let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> DVal.DBool True
let helpers = { emit = \(_ : DVal) -> \(_ : DVal) -> {=} }
let _ = helpers.emit (process (DVal.DInteger +1)) (DVal.DInteger +42)
in {=}
