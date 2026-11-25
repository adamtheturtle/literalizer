pub type GVal {
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([])
  let _ = my_data
}
