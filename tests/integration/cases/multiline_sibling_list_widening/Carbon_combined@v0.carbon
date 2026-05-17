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
    {.key = "omap_value", .val = CVal.Map(({.key = "first", .val = CVal.Int(1)}))},
    {.key = "sibling_lists", .val = CVal.Map(({.key = "numbers", .val = CVal.Arr((CVal.Int(1), CVal.Int(2)))}, {.key = "strings", .val = CVal.Arr((CVal.Str("x"), CVal.Str("y")))}))},
    {.key = "ref_marker_present", .val = CVal.Arr((CVal.Str("$keep"), CVal.Str("z")))},
  ));
  my_data = CVal.Map((
    {.key = "omap_value", .val = CVal.Map(({.key = "first", .val = CVal.Int(1)}))},
    {.key = "sibling_lists", .val = CVal.Map(({.key = "numbers", .val = CVal.Arr((CVal.Int(1), CVal.Int(2)))}, {.key = "strings", .val = CVal.Arr((CVal.Str("x"), CVal.Str("y")))}))},
    {.key = "ref_marker_present", .val = CVal.Arr((CVal.Str("$keep"), CVal.Str("z")))},
  ));
  let _: CVal = my_data;
}
