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
    CVal.Float(-0.0),
    CVal.Float(1.5),
  ));
  my_data = CVal.Arr((
    CVal.Float(-0.0),
    CVal.Float(1.5),
  ));
  let _: CVal = my_data;
}
