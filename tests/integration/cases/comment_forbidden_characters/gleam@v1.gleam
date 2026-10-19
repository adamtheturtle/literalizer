pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(1)),  // tab	here and bidi <U+202E>after
    #("b", GInt(2)),
  ])
  let _ = my_data
}
