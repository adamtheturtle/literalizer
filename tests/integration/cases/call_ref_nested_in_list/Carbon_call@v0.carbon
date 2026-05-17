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
  let my_other: CVal = CVal.Int(7);
  process(CVal.Arr((my_var, CVal.Int(42), CVal.Str("static"))));
  process(CVal.Arr((my_other, CVal.Int(7), CVal.Str("label"))));
}
