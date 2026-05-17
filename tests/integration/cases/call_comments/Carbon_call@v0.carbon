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
fn Run() {
  // Test cases
  process(CVal.Str("hello"));  // single word
  process(CVal.Str("hello world"));  // two words
  // trailing comment
}
