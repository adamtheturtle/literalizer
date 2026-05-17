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
fn process(value: CVal) {}
fn emit(_call: CVal, _zip: CVal) {}
fn Run() {
  emit(process(CVal.Str("hello")), CVal.Bool(true));
  emit(process(CVal.Int(42)), CVal.Bool(false));
}
