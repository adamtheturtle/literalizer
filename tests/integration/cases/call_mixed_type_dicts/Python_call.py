class _MType:
    def Op(self, *_args: object, **_kwargs: object) -> object: ...
m = _MType()
m.Op(operation={"type": "create", "pr_id": "pr_1", "draft": True})
m.Op(operation={"type": "create", "pr_id": "pr_2"})
