pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("i32_below", GInt(-2147483649)),
    #("i32_minimum", GInt(-2147483648)),
    #("i32_above", GInt(-2147483647)),
    #("i32_maximum", GInt(2147483647)),
    #("i32_over", GInt(2147483648)),
    #("i64_minimum", GInt(-9223372036854775808)),
    #("i64_maximum", GInt(9223372036854775807)),
  ])
  let _ = my_data
}
