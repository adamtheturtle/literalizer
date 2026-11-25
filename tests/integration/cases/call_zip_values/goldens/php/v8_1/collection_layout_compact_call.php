<?php
function process($value) {}
function emit($_call, $_zip) {}
emit(process(value: "hello"), true);
emit(process(value: 42), false);
