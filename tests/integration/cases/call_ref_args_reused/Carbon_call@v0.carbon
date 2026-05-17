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
fn process(data: CVal, count: CVal) {}
fn Run() {
  let single_var: CVal = CVal.Arr((
    CVal.Int(4),
    CVal.Int(5),
    CVal.Int(6),
  ));
  let repeated_var: CVal = CVal.Int(1);
  process(repeated_var, CVal.Int(1));
  process(single_var, CVal.Int(0));
  process(repeated_var, CVal.Int(8));
}
