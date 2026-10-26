pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(0o777777777777777777777)),
    #("b", GInt(0o1000000000000000000000)),
  ])
  let _ = my_data
}
