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
  let my_data: CVal = CVal.Arr((
    CVal.Map(({.key = "id", .val = CVal.Int(1)}, {.key = "label", .val = CVal.Str("first")}, {.key = "tags", .val = CVal.Arr(())})),
    CVal.Map(({.key = "id", .val = CVal.Int(2)}, {.key = "label", .val = CVal.Str("second")}, {.key = "tags", .val = CVal.Arr(())})),
    CVal.Map(({.key = "id", .val = CVal.Int(3)}, {.key = "label", .val = CVal.Str("third")}, {.key = "tags", .val = CVal.Arr(())})),
  ));
  let _: CVal = my_data;
}
