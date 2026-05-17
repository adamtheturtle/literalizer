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
    {.key = "items", .val = CVal.Arr((CVal.Map(({.key = "id", .val = CVal.Int(1)})), CVal.Map(({.key = "id", .val = CVal.Int(2)}, {.key = "count", .val = CVal.Int(10)})), CVal.Map(({.key = "id", .val = CVal.Int(3)}, {.key = "count", .val = CVal.Int(20)}))))},
  ));
  let _: CVal = my_data;
}
