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
    CVal.Map(({.key = "first", .val = CVal.Str("Alice")}, {.key = "last", .val = CVal.Str("Smith")})),
    CVal.Map(({.key = "first", .val = CVal.Str("Bob")}, {.key = "last", .val = CVal.Str("Jones")})),
  ));
  my_data = CVal.Arr((
    CVal.Map(({.key = "first", .val = CVal.Str("Alice")}, {.key = "last", .val = CVal.Str("Smith")})),
    CVal.Map(({.key = "first", .val = CVal.Str("Bob")}, {.key = "last", .val = CVal.Str("Jones")})),
  ));
  let _: CVal = my_data;
}
