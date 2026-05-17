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
    {.key = "name", .val = CVal.Str("Alice")},
    {.key = "scores", .val = CVal.Arr((CVal.Int(10), CVal.Int(20), CVal.Int(30)))},
  ));
  my_data = CVal.Map((
    {.key = "name", .val = CVal.Str("Alice")},
    {.key = "scores", .val = CVal.Arr((CVal.Int(10), CVal.Int(20), CVal.Int(30)))},
  ));
  let _: CVal = my_data;
}
