<?php
class ThrottlerType { function check($user_id, $ts) {} }
$throttler = new ThrottlerType();
function emit($_arg) {}
emit($throttler->check(user_id: "user_1", ts: 1000.0));
emit($throttler->check(user_id: "user_2", ts: 2000.5));
