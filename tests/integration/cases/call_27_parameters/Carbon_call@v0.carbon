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
fn process(p0: CVal, p1: CVal, p2: CVal, p3: CVal, p4: CVal, p5: CVal, p6: CVal, p7: CVal, p8: CVal, p9: CVal, p10: CVal, p11: CVal, p12: CVal, p13: CVal, p14: CVal, p15: CVal, p16: CVal, p17: CVal, p18: CVal, p19: CVal, p20: CVal, p21: CVal, p22: CVal, p23: CVal, p24: CVal, p25: CVal, p26: CVal) {}
fn Run() {
  process(CVal.Int(0), CVal.Int(1), CVal.Int(2), CVal.Int(3), CVal.Int(4), CVal.Int(5), CVal.Int(6), CVal.Int(7), CVal.Int(8), CVal.Int(9), CVal.Int(10), CVal.Int(11), CVal.Int(12), CVal.Int(13), CVal.Int(14), CVal.Int(15), CVal.Int(16), CVal.Int(17), CVal.Int(18), CVal.Int(19), CVal.Int(20), CVal.Int(21), CVal.Int(22), CVal.Int(23), CVal.Int(24), CVal.Int(25), CVal.Int(26));
}
