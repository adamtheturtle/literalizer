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
    CVal.Str("C:\\path\\to\\file"),
    CVal.Str("back\\\\slash"),
    CVal.Str("hello \\\"world\\\""),
    CVal.Str("path\\to \"# file"),
    CVal.Str("trailing\\"),
    CVal.Str("both \"quotes''' here"),
    CVal.Str("line1\\nline2\nwith newline"),
  ));
  my_data = CVal.Arr((
    CVal.Str("C:\\path\\to\\file"),
    CVal.Str("back\\\\slash"),
    CVal.Str("hello \\\"world\\\""),
    CVal.Str("path\\to \"# file"),
    CVal.Str("trailing\\"),
    CVal.Str("both \"quotes''' here"),
    CVal.Str("line1\\nline2\nwith newline"),
  ));
  let _: CVal = my_data;
}
