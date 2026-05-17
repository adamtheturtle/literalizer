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
    {.key = "metrics", .val = CVal.Map(({.key = "count", .val = CVal.Int(100)}, {.key = "rate", .val = CVal.Int(50)}))},
    {.key = "flags", .val = CVal.Map(({.key = "retries", .val = CVal.Int(3)}, {.key = "timeout", .val = CVal.Int(30)}))},
  ));
  my_data = CVal.Map((
    {.key = "metrics", .val = CVal.Map(({.key = "count", .val = CVal.Int(100)}, {.key = "rate", .val = CVal.Int(50)}))},
    {.key = "flags", .val = CVal.Map(({.key = "retries", .val = CVal.Int(3)}, {.key = "timeout", .val = CVal.Int(30)}))},
  ));
  let _: CVal = my_data;
}
