proc process {args} {return {}}
proc log.emit {args} {}
log.emit [process "hello"]
log.emit [process 42]
log.emit [process 1]
