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
    CVal.Int(0xf4240),
    CVal.Int(-0x4d2),
    CVal.Int(0xff),
    CVal.Int(-0xa),
  ));
  let _: CVal = my_data;
}
