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
  var my_data: CVal = CVal.Arr((
    CVal.Int(1000000),
    CVal.Int(-1234),
    CVal.Int(255),
    CVal.Int(-10),
  ));
  my_data = CVal.Arr((
    CVal.Int(1000000),
    CVal.Int(-1234),
    CVal.Int(255),
    CVal.Int(-10),
  ));
  let _: CVal = my_data;
}
