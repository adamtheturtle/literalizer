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
    {.key = "lint", .val = CVal.Arr((CVal.Int(2), CVal.Arr((CVal.Int(1)))))},
    {.key = "test", .val = CVal.Arr((CVal.Int(5), CVal.Arr((CVal.Int(7)))))},
  ));
  my_data = CVal.Map((
    {.key = "lint", .val = CVal.Arr((CVal.Int(2), CVal.Arr((CVal.Int(1)))))},
    {.key = "test", .val = CVal.Arr((CVal.Int(5), CVal.Arr((CVal.Int(7)))))},
  ));
  let _: CVal = my_data;
}
