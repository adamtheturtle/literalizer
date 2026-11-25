pub type GVal1 {
  GVal1(value: Int)
}
pub type GVal0 {
  GVal0(section: GVal1)
}

pub fn main() {
  let my_data = GVal0(
    section: GVal1(
      value: 1,
    ),
  )
  let _ = my_data
}
