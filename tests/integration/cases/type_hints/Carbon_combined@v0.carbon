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
    {.key = "name", .val = CVal.Str("Alice")},
    {.key = "age", .val = CVal.Int(30)},
    {.key = "active", .val = CVal.Bool(true)},
    {.key = "score", .val = CVal.Nil},
    {.key = "joined", .val = CVal.Int(1705276800)},
    {.key = "last_login", .val = CVal.Int(1705321800)},
    {.key = "avatar", .val = CVal.Str("48656c6c6f")},
  ));
  my_data = CVal.Map((
    {.key = "name", .val = CVal.Str("Alice")},
    {.key = "age", .val = CVal.Int(30)},
    {.key = "active", .val = CVal.Bool(true)},
    {.key = "score", .val = CVal.Nil},
    {.key = "joined", .val = CVal.Int(1705276800)},
    {.key = "last_login", .val = CVal.Int(1705321800)},
    {.key = "avatar", .val = CVal.Str("48656c6c6f")},
  ));
  let _: CVal = my_data;
}
