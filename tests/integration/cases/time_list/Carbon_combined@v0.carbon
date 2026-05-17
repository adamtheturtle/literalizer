choice CVal {
  Nil,
  Bool(bool),
  Int(i64),
  UInt(u64),
  Float(f64),
  Str(Core.String),
  Arr(Core.Array(CVal)),
  Map(Core.Array({.key: Core.String, .val: CVal})),
  Set(Core.Array(CVal)),
}
fn Run() {
  var my_data: CVal = CVal.Map((
    {.key = "times", .val = CVal.Arr((CVal.Str("09:30:00"), CVal.Str("17:45:00"), CVal.Str("23:59:59")))},
  ));
  my_data = CVal.Map((
    {.key = "times", .val = CVal.Arr((CVal.Str("09:30:00"), CVal.Str("17:45:00"), CVal.Str("23:59:59")))},
  ));
  let _: CVal = my_data;
}
