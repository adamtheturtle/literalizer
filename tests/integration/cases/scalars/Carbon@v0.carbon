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
    CVal.Int(42),
    CVal.Float(3.14),
    CVal.Bool(true),
    CVal.Bool(false),
    CVal.Str("hello \"world\""),
  ));
  let _: CVal = my_data;
}
