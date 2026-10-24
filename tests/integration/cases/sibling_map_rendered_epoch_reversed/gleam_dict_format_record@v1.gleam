pub type GVal1 {
  GVal1(k: Int)
}
pub type GVal2 {
  GVal2(k: String)
}
pub type GVal0 {
  GVal0(b: GVal1, a: GVal2)
}

pub fn main() {
  let my_data = GVal0(
    b: GVal1(
      k: 1,
    ),
    a: GVal2(
      k: "2040-01-01T00:00:00+00:00",
    ),
  )
  let _ = my_data
}
