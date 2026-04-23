declare const mgr: any;
mgr.Op({ operation: {"type": "create", "pr_id": "pr_1", "draft": true} });
mgr.Op({ operation: {"type": "create", "pr_id": "pr_2"} });
export {};
