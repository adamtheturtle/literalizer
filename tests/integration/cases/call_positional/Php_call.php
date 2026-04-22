<?php
class ThrottlerType { function check($user_id, $ts) {} }
$throttler = new ThrottlerType();
function emit($_arg) {}
emit($throttler->check("user_1", 1000.0));
emit($throttler->check("user_2", 2000.5));
