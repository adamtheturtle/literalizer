class ThrottlerType_ { [object] check([object] $user_id, [object] $ts) { return $null } }
$throttler = [ThrottlerType_]::new()
function emit {}
emit($throttler.check("user_1", 1000.0))
emit($throttler.check("user_2", 2000.5))
