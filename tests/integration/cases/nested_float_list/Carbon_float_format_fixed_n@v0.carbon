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
    CVal.Arr((CVal.Float(1.500000), CVal.Float(2.500000))),
    CVal.Arr((CVal.Float(3.500000), CVal.Float(4.500000))),
  ));
  let _: CVal = my_data;
}
