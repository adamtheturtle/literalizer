<?php
function process($value) {}
function emit($_call, $_zip) {}
emit(process(value: "hello"), 1);
emit(process(value: 42), 0);
