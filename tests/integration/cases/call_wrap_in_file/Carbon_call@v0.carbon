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
fn process(a: CVal, b: CVal) {}
fn Run() {
  process(CVal.Int(1), CVal.Int(2));
  process(CVal.Int(3), CVal.Int(4));
}
