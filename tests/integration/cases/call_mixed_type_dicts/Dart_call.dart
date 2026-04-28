class _MgrType { dynamic op({dynamic operation}) => null; }
class _AppType { final mgr = _MgrType(); }
final app = _AppType();
final my_data = null;
void main() {
    app.mgr.op(operation: <String, dynamic>{"type": "create", "pr_id": "pr_1", "draft": true});
    app.mgr.op(operation: <String, dynamic>{"type": "create", "pr_id": "pr_2"});
}
