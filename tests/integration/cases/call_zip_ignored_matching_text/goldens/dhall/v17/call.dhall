let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let process = \(_ : DVal) -> DVal.DBool True
let _ = process (DVal.DText "time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)")
in {=}
