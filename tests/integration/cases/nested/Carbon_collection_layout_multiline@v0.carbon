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
    {.key = "users", .val = CVal.Arr((
      CVal.Map((
        {.key = "name", .val = CVal.Str("Bob")},
        {.key = "tags", .val = CVal.Arr((
          CVal.Str("admin"),
          CVal.Str("user"),
        ))},
      )),
      CVal.Map((
        {.key = "name", .val = CVal.Str("Carol")},
        {.key = "tags", .val = CVal.Arr((
          CVal.Str("guest"),
        ))},
      )),
    ))},
  ));
  let _: CVal = my_data;
}
