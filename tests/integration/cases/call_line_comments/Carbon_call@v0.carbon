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
  process(CVal.Str("Dune"));  // first edition
  process(CVal.Str("Solaris"));
  process(CVal.Str("Neuromancer"));  // cyberpunk
}
