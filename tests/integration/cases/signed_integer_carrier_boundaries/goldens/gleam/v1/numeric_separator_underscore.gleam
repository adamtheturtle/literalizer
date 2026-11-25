pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("i32_below", GInt(-2_147_483_649)),
    #("i32_minimum", GInt(-2_147_483_648)),
    #("i32_above", GInt(-2_147_483_647)),
    #("i32_maximum", GInt(2_147_483_647)),
    #("i32_over", GInt(2_147_483_648)),
    #("i64_minimum", GInt(-9_223_372_036_854_775_808)),
    #("i64_maximum", GInt(9_223_372_036_854_775_807)),
  ])
  let _ = my_data
}
