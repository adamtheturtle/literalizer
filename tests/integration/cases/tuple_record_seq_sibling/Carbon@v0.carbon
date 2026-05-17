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
  let my_data: CVal = CVal.Map((
    {.key = "scores", .val = CVal.Arr((CVal.Int(10), CVal.Int(20), CVal.Int(30)))},
    {.key = "args", .val = CVal.Arr((CVal.Int(1), CVal.Str("email"), CVal.Str("a@gmail.com"), CVal.Int(100)))},
  ));
  let _: CVal = my_data;
}
