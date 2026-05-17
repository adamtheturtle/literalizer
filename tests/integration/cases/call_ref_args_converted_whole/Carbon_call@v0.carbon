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
  let my_var: CVal = CVal.Arr((
    CVal.Int(1),
    CVal.Int(2),
    CVal.Int(3),
  ));
  process(my_var);
}
