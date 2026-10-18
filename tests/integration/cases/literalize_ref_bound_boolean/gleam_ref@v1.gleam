pub type GVal {
  GBool(Bool)
}

pub fn main() {
  let ref_flag = GBool(True)
  let my_data = ref_flag
  let _ = my_data
}
