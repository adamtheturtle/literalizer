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
    {.key = "call", .val = CVal.Str("send")},
    {.key = "args", .val = CVal.Arr((CVal.Int(1), CVal.Str("email"), CVal.Str("a@gmail.com"), CVal.Int(100)))},
  ));
  my_data = CVal.Map((
    {.key = "call", .val = CVal.Str("send")},
    {.key = "args", .val = CVal.Arr((CVal.Int(1), CVal.Str("email"), CVal.Str("a@gmail.com"), CVal.Int(100)))},
  ));
  let _: CVal = my_data;
}
