pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("i32_below", GInt(-{0o20000000001})),
    #("i32_minimum", GInt(-{0o20000000000})),
    #("i32_above", GInt(-{0o17777777777})),
    #("i32_maximum", GInt(0o17777777777)),
    #("i32_over", GInt(0o20000000000)),
    #("i64_minimum", GInt(-{0o1000000000000000000000})),
    #("i64_maximum", GInt(0o777777777777777777777)),
  ])
  let _ = my_data
}
