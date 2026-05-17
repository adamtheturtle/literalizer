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
fn process(value: CVal, count: CVal) {}
fn Run() {
  let my_int: CVal = CVal.Int(1);
  let my_bool: CVal = CVal.Bool(true);
  let my_float: CVal = CVal.Float(3.14);
  let my_list: CVal = CVal.Arr((
    CVal.Int(1),
    CVal.Int(2),
    CVal.Int(3),
  ));
  process(my_int, CVal.Int(42));
  process(my_bool, CVal.Int(7));
  process(my_float, CVal.Int(9));
  process(my_list, CVal.Int(1));
}
