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
fn process(data: CVal, count: CVal) {}
fn Run() {
  let my_ints: CVal = CVal.Arr((
    CVal.Int(1),
    CVal.Int(2),
    CVal.Int(3),
  ));
  let my_strings: CVal = CVal.Arr((
    CVal.Str("a"),
    CVal.Str("b"),
  ));
  let my_empty: CVal = CVal.Arr(());
  process(my_ints, CVal.Int(42));
  process(my_strings, CVal.Int(7));
  process(my_empty, CVal.Int(99));
}
