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
  let my_var: CVal = CVal.Arr((
    CVal.Int(1),
    CVal.Int(2),
    CVal.Int(3),
  ));
  let my_other: CVal = CVal.Arr((
    CVal.Int(4),
    CVal.Int(5),
    CVal.Int(6),
  ));
  process(my_var, CVal.Int(42));
  process(my_other, CVal.Int(7));
}
