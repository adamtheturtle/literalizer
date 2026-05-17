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
fn Run() {
  let my_data: CVal = CVal.Arr((
    CVal.Float(0.000000),
    CVal.Float(1.000000),
    CVal.Float(1500.000000),
    CVal.Float(0.001000),
  ));
  let _: CVal = my_data;
}
