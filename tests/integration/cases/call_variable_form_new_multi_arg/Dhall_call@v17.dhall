let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let record_entry = \(_ : DVal) -> \(_ : DVal) -> \(_ : DVal) -> DVal.DBool True
let my_data = record_entry (DVal.DText "a") (DVal.DInteger +1) (DVal.DBool True) in my_data
