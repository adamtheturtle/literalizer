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
    {.key = "first", .val = CVal.Str("one")},
    {.key = "second", .val = CVal.Str("two")},
    {.key = "third", .val = CVal.Str("three")},
  ));
  let _: CVal = my_data;
}
