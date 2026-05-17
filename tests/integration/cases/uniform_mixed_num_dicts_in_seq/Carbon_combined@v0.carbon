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
    CVal.Map(({.key = "x", .val = CVal.Int(1)}, {.key = "y", .val = CVal.Float(2.5)})),
    CVal.Map(({.key = "x", .val = CVal.Int(3)}, {.key = "y", .val = CVal.Float(4.0)})),
  ));
  my_data = CVal.Arr((
    CVal.Map(({.key = "x", .val = CVal.Int(1)}, {.key = "y", .val = CVal.Float(2.5)})),
    CVal.Map(({.key = "x", .val = CVal.Int(3)}, {.key = "y", .val = CVal.Float(4.0)})),
  ));
  let _: CVal = my_data;
}
