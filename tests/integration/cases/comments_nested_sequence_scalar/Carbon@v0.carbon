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
    CVal.Arr((CVal.Str("ADD"), CVal.Str("alice"), CVal.Str("hello"))),
    CVal.Arr((CVal.Str("DEL"), CVal.Str("bob"), CVal.Str("5"))),  // removes "world"
  ));
  let _: CVal = my_data;
}
