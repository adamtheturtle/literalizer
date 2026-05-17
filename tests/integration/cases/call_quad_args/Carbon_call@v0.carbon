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
fn process(a: CVal, b: CVal, c: CVal, d: CVal) {}
fn Run() {
  process(CVal.Int(1), CVal.Int(2), CVal.Int(3), CVal.Int(4));
  process(CVal.Int(5), CVal.Int(6), CVal.Int(7), CVal.Int(8));
}
