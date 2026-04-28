process() { :; }
log.emit() { :; }
log.emit "$(process "hello")"
log.emit "$(process 42)"
log.emit "$(process true)"
