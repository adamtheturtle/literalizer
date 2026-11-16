<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [1, 1, 1, 2];
    if ($event_index >= 4 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function process(int $value): int { observe_event(1); observe_event($value); return $value + 100; }
function verify_events(): void { global $event_index; if ($event_index !== 4) throw new RuntimeException("missing receiver events"); }
process(value: 1);  // trail \ .
process(value: 2);  // second
verify_events();
