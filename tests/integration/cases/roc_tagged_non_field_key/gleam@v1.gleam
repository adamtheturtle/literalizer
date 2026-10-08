pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("not-a-field", GInt(1)),
  ])
  let _ = my_data
}
