use std::collections::HashMap;
#[derive(Clone)]
pub struct Record1 {
    pub r#type: Option<&'static str>,
    pub pr_id: &'static str,
    pub draft: Option<bool>,
    pub missing: Option<Option<()>>,
    pub status: Option<Option<()>>,
}
#[derive(Clone)]
pub struct Record0 {
    pub name: &'static str,
    pub input: Record1,
    pub expected: HashMap<&'static str, &'static str>,
}
fn main() {
    let my_data = vec![
        Record0 { name: "test_1", input: Record1 { r#type: Some("create"), pr_id: "pr_1", draft: Some(true), missing: Some(None::<()>), status: None }, expected: HashMap::from([("pr_id", "pr_1"), ("status", "draft")]) },
        Record0 { name: "test_2", input: Record1 { r#type: Some("publish"), pr_id: "pr_1", draft: None, missing: None, status: None }, expected: HashMap::from([("error", "invalid_operation")]) },
    ];
    let _ = &my_data;
}
