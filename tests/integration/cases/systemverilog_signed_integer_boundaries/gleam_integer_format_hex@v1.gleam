pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("i32_below", GInt(-{0x80000001})),
    #("i32_minimum", GInt(-{0x80000000})),
    #("i32_above", GInt(-{0x7fffffff})),
    #("i32_maximum", GInt(0x7fffffff)),
    #("i32_over", GInt(0x80000000)),
    #("i64_minimum", GInt(-{0x8000000000000000})),
    #("i64_maximum", GInt(0x7fffffffffffffff)),
  ])
  let _ = my_data
}
