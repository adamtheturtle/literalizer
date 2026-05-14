pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("metrics", GDict([#("count", GInt(100)), #("rate", GInt(50))])),
    #("flags", GDict([#("retries", GInt(3)), #("timeout", GInt(30))])),
  ])
  let my_data = GDict([
    #("metrics", GDict([#("count", GInt(100)), #("rate", GInt(50))])),
    #("flags", GDict([#("retries", GInt(3)), #("timeout", GInt(30))])),
  ])
  let _ = my_data
}
