class _MgrType:
    def Op(self, *_args: object, **_kwargs: object) -> object: ...
mgr = _MgrType()
mgr.Op(operation={"type": "create", "pr_id": "pr_1", "draft": True})
mgr.Op(operation={"type": "create", "pr_id": "pr_2"})
