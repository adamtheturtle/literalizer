<?php
function process($value) {}
function emit($_call, $_zip) {}
emit(process(value: "hello"), "one");
emit(process(value: 42), "zero");
