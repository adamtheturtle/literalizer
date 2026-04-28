class _ClientType { dynamic fetch({dynamic payload}) => null; }
class _AppType { final client = _ClientType(); }
final app = _AppType();
dynamic emit({dynamic _arg}) => null;
emit(app.client.fetch(payload: "hello"));
emit(app.client.fetch(payload: 42));
emit(app.client.fetch(payload: true));
