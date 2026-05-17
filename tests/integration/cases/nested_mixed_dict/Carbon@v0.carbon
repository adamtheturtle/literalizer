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
    {.key = "outer", .val = CVal.Map(({.key = "a", .val = CVal.Int(1)}, {.key = "b", .val = CVal.Str("x")}, {.key = "c", .val = CVal.Nil}))},
  ));
  let _: CVal = my_data;
}
