struct Record1 { let count: Int; let rate: Int }
struct Record2 { let retries: Int; let timeout: Int }
struct Record0 { let metrics: Record1; let flags: Record2 }
let my_data: Any = Record0(
    metrics: Record1(
        count: 100,
        rate: 50,
    ),
    flags: Record2(
        retries: 3,
        timeout: 30,
    ),
)
