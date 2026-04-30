from __future__ import annotations
class _MgrType:
    def op(self, *_args: object, **_kwargs: object) -> object: ...
class _AppType:
    mgr = _MgrType()
app = _AppType()
app.mgr.op(operation={"type": "create", "pr_id": "pr_1", "draft": True})
app.mgr.op(operation={"type": "create", "pr_id": "pr_2"})
