pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("__proto__", GDict([#("x", GInt(1))])),
    #("ordinary", GInt(2)),
  ])
  let _ = my_data
}
