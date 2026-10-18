pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let shared_time = GStr("12:30:15+02:00")
  let my_data = GDict([
    #("x", shared_time),
  ])
  let _ = my_data
}
