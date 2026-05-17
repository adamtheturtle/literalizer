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
    // line 1
    // line 2
    CVal.Str("a"),
  ));
  my_data = CVal.Arr((
    // line 1
    // line 2
    CVal.Str("a"),
  ));
  let _: CVal = my_data;
}
