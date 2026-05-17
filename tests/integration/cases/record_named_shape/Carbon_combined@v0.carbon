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
  var my_data: CVal = CVal.Arr((
    CVal.Map(({.key = "id", .val = CVal.Int(100)}, {.key = "description", .val = CVal.Str("first task")}, {.key = "is_done", .val = CVal.Bool(false)}, {.key = "blocks", .val = CVal.Arr((CVal.Int(102), CVal.Int(103)))})),
    CVal.Map(({.key = "id", .val = CVal.Int(101)}, {.key = "description", .val = CVal.Str("second task")}, {.key = "is_done", .val = CVal.Bool(true)}, {.key = "blocks", .val = CVal.Arr((CVal.Int(100)))})),
  ));
  my_data = CVal.Arr((
    CVal.Map(({.key = "id", .val = CVal.Int(100)}, {.key = "description", .val = CVal.Str("first task")}, {.key = "is_done", .val = CVal.Bool(false)}, {.key = "blocks", .val = CVal.Arr((CVal.Int(102), CVal.Int(103)))})),
    CVal.Map(({.key = "id", .val = CVal.Int(101)}, {.key = "description", .val = CVal.Str("second task")}, {.key = "is_done", .val = CVal.Bool(true)}, {.key = "blocks", .val = CVal.Arr((CVal.Int(100)))})),
  ));
  let _: CVal = my_data;
}
