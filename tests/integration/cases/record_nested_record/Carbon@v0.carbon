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
    {.key = "id", .val = CVal.Int(1)},
    {.key = "owner", .val = CVal.Map(({.key = "name", .val = CVal.Str("Alice")}, {.key = "age", .val = CVal.Int(30)}))},
  ));
  let _: CVal = my_data;
}
