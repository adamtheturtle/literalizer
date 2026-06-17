let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let record = \(_ : DVal) -> DVal.DBool True
let flush = \(_ : DVal) -> {=}
let _ = record (DVal.DInteger +42)
let _ = flush (DVal.DInteger +3)
in {=}
