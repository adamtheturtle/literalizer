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
    // before apple
    CVal.Str("apple"),
    CVal.Str("banana"),  // banana inline
    // trailing
  ));
  my_data = CVal.Set((
    // before apple
    CVal.Str("apple"),
    CVal.Str("banana"),  // banana inline
    // trailing
  ));
  let _: CVal = my_data;
}
