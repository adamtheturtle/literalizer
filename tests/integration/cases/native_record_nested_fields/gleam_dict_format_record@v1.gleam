pub type GVal1 {
  GVal1(name: String, active: Bool)
}
pub type GVal2 {
  GVal2(name: String, score: Float)
}
pub type GVal0 {
  GVal0(owner: GVal1, members: List(GVal2))
}

pub fn main() {
  let my_data = GVal0(
    owner: GVal1(
      name: "Ada",
      active: False,
    ),
    members: [
      GVal2(
        name: "Ada",
        score: 1.5,
      ),
      GVal2(
        name: "Bob",
        score: 2.5,
      ),
    ],
  )
  let _ = my_data
}
