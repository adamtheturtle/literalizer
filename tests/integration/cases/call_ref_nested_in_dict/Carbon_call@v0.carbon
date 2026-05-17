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
fn process(data: CVal) {}
fn Run() {
  let my_var: CVal = CVal.Int(42);
  process(CVal.Map(({.key = "key", .val = my_var}, {.key = "count", .val = CVal.Int(42)})));
}
