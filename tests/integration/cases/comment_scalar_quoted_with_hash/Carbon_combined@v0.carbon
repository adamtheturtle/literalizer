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
  // note
  var my_data: CVal = CVal.Str("hello # world");
  // note
  my_data = CVal.Str("hello # world");
  let _: CVal = my_data;
}
