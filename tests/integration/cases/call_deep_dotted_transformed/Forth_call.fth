: app ;
: app.client ;
: app.client.fetch ;
: emit ;
emit(app.client.fetch(s\" hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
