<?php
function process($value) {}
class LogType { function emit($_arg) {} }
$log = new LogType();
log.emit(process(value: "hello"));
log.emit(process(value: 42));
log.emit(process(value: true));
