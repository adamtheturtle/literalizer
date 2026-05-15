<?php
function process($value) {}
class TracerType { function emit($_arg) {} }
$tracer = new TracerType();
tracer.emit(process(value: "hello"));
tracer.emit(process(value: 42));
tracer.emit(process(value: true));
