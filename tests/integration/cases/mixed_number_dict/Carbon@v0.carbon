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
    {.key = "a", .val = CVal.Int(1)},
    {.key = "b", .val = CVal.Float(2.5)},
    {.key = "c", .val = CVal.Int(3)},
  ));
  let _: CVal = my_data;
}
