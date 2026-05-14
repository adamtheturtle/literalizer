pub type GVal {
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("morning", "09:30:00"),
    #("afternoon", "14:15:00"),
    #("evening", "23:59:59"),
  ])
  let my_data = GDict([
    #("morning", "09:30:00"),
    #("afternoon", "14:15:00"),
    #("evening", "23:59:59"),
  ])
  let _ = my_data
}
