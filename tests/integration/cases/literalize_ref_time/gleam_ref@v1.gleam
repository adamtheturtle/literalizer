pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_time = GStr("01:02:03")
  let my_data = GDict([
    #("x", my_time),
  ])
  let _ = my_data
}
