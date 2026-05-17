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
  var my_data: CVal = CVal.Set((
    CVal.Str("apple"),
    CVal.Str("banana"),
    CVal.Str("cherry"),
  ));
  my_data = CVal.Set((
    CVal.Str("apple"),
    CVal.Str("banana"),
    CVal.Str("cherry"),
  ));
  let _: CVal = my_data;
}
