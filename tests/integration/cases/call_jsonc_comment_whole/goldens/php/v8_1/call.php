<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [1, 42];
    if ($event_index >= 2 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function f(int $a): int { observe_event(1); observe_event($a); return $a + 100; }
function verify_events(): void { global $event_index; if ($event_index !== 2) throw new RuntimeException("missing receiver events"); }
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(a: 42);
verify_events();
