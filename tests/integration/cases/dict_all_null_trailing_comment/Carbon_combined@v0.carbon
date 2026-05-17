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
  var my_data: CVal = CVal.Map((
    {.key = "a", .val = CVal.Nil},
    {.key = "b", .val = CVal.Nil},
    // trailing
  ));
  my_data = CVal.Map((
    {.key = "a", .val = CVal.Nil},
    {.key = "b", .val = CVal.Nil},
    // trailing
  ));
  let _: CVal = my_data;
}
