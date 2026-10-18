pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("within_i32", GInt(1705320000)),
    #("beyond_i32", GInt(4085195400)),
  ])
  let _ = my_data
}
