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
    CVal.Arr((CVal.Map(({.key = "name", .val = CVal.Str("Alice")})), CVal.Map(({.key = "name", .val = CVal.Str("Bob")})))),
    CVal.Arr((CVal.Map(({.key = "name", .val = CVal.Str("Charlie")})), CVal.Map(({.key = "name", .val = CVal.Str("Dave")})))),
  ));
  let _: CVal = my_data;
}
