struct Record1 { let kind: String; let pr_id: String }
struct Record0 { let name: String; let input: Record1; let expected: [String: Any?] }
let my_data = [
    Record0(
        name: "test_1",
        input: Record1(
            kind: "create",
            pr_id: "pr_1",
        ),
        expected: [
            "pr_id": "pr_1",
            "status": "draft",
        ],
    ),
    Record0(
        name: "test_2",
        input: Record1(
            kind: "publish",
            pr_id: "pr_1",
        ),
        expected: [
            "error": "invalid_operation",
        ],
    ),
]
