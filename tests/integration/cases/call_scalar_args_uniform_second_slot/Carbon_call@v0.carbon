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
fn process(value: CVal, label: CVal) {}
fn Run() {
  process(CVal.Str("hello"), CVal.Str("a"));
  process(CVal.Int(42), CVal.Str("b"));
  process(CVal.Bool(true), CVal.Str("c"));
}
