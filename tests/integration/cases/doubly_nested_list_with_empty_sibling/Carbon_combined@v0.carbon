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
    CVal.Arr((CVal.Arr((CVal.Int(1), CVal.Int(2))))),
    CVal.Arr(()),
    CVal.Arr((CVal.Arr((CVal.Int(3), CVal.Int(4))))),
  ));
  my_data = CVal.Arr((
    CVal.Arr((CVal.Arr((CVal.Int(1), CVal.Int(2))))),
    CVal.Arr(()),
    CVal.Arr((CVal.Arr((CVal.Int(3), CVal.Int(4))))),
  ));
  let _: CVal = my_data;
}
