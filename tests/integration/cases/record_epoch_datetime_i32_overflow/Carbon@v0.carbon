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
  let my_data: CVal = CVal.Map((
    {.key = "within_i32", .val = CVal.Int(1705320000)},
    {.key = "beyond_i32", .val = CVal.Int(4085195400)},
  ));
  let _: CVal = my_data;
}
