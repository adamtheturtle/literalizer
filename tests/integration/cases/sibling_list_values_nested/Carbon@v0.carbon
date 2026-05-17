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
    {.key = "lint", .val = CVal.Arr((CVal.Int(2), CVal.Arr(())))},
    {.key = "test", .val = CVal.Arr((CVal.Int(5), CVal.Arr((CVal.Str("compile")))))},
  ));
  let _: CVal = my_data;
}
