struct Record1 { let x: Int; let y: Any? }
struct Record2 { let x: Any?; let y: Any? }
struct Record3 { let x: Int; let y: Int }
struct Record0 { let nullable: Record1; let null_fields: Record2; let plain: Record3 }
let nullable: Record1 = Record1(
    x: 1,
    y: nil,
)
let nullFields: Record2 = Record2(
    x: nil,
    y: nil,
)
let plain: Record3 = Record3(
    x: 1,
    y: 2,
)
let my_data: Record0 = Record0(
    nullable: nullable,
    null_fields: nullFields,
    plain: plain,
)
