struct Record0 { let name: String; let input: [String: Any]; let expected: [String: Any] }
let my_data: Any = [
    Record0(name: "test_1", input: ["type": "create", "pr_id": "pr_1", "draft": true, "missing": nil], expected: ["pr_id": "pr_1", "status": "draft"]),
    Record0(name: "test_2", input: ["type": "publish", "pr_id": "pr_1"], expected: ["error": "invalid_operation"]),
]
