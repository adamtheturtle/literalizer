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
  let my_data: CVal = CVal.Set((
    CVal.Str("apple"),  // inline comment
    // before banana
    CVal.Str("banana"),
    // trailing
  ));
  let _: CVal = my_data;
}
