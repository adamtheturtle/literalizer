let DVal = < DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >
let obj = { ZVal = \(_ : DVal) -> DVal.DBool True }
let my_data = obj.ZVal (DVal.DInteger +42) // note in my_data
