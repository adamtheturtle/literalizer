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
    {.key = "name", .val = CVal.Str("Alice")},
    {.key = "tags", .val = CVal.Set((CVal.Bool(true), CVal.Int(42), CVal.Str("apple")))},
  ));
  let _: CVal = my_data;
}
