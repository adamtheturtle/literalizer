pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // heading
    #("count", GInt(2)),
  ])
  let _ = my_data
}
