class OuterType_ { [object] inner([object] $outer, [object] $n) { return $null } }
$outer = [OuterType_]::new()
$outer.inner(1, 2)
