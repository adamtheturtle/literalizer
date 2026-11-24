pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(0o1)),
    #("b", GInt(0o20000000000000)),
  ])
  let _ = my_data
}
