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
    {.key = "level1", .val = CVal.Map(({.key = "level2", .val = CVal.Map(({.key = "level3", .val = CVal.Map(({.key = "level4", .val = CVal.Map(({.key = "value", .val = CVal.Str("deep")}, {.key = "items", .val = CVal.Arr((CVal.Str("a"), CVal.Str("b")))}))}))}, {.key = "sibling", .val = CVal.Int(42)}))}, {.key = "tags", .val = CVal.Arr((CVal.Map(({.key = "name", .val = CVal.Str("tag1")}, {.key = "meta", .val = CVal.Map(({.key = "priority", .val = CVal.Int(1)}, {.key = "labels", .val = CVal.Arr((CVal.Str("x"), CVal.Str("y")))}))}))))}))},
  ));
  my_data = CVal.Map((
    {.key = "level1", .val = CVal.Map(({.key = "level2", .val = CVal.Map(({.key = "level3", .val = CVal.Map(({.key = "level4", .val = CVal.Map(({.key = "value", .val = CVal.Str("deep")}, {.key = "items", .val = CVal.Arr((CVal.Str("a"), CVal.Str("b")))}))}))}, {.key = "sibling", .val = CVal.Int(42)}))}, {.key = "tags", .val = CVal.Arr((CVal.Map(({.key = "name", .val = CVal.Str("tag1")}, {.key = "meta", .val = CVal.Map(({.key = "priority", .val = CVal.Int(1)}, {.key = "labels", .val = CVal.Arr((CVal.Str("x"), CVal.Str("y")))}))}))))}))},
  ));
  let _: CVal = my_data;
}
