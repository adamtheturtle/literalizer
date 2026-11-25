pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(1)),
    #("b", GInt(1_099_511_627_776)),
  ])
  let _ = my_data
}
