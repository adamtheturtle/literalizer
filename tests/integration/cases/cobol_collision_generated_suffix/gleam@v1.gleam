pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a-b", GInt(1)),
    #("a b", GInt(2)),
    #("a-b-2", GInt(3)),
  ])
  let _ = my_data
}
