<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [1, -1, 1, -2, 1, -3];
    if ($event_index >= 6 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function process(int $value): int { observe_event(1); observe_event($value); return $value + 100; }
function verify_events(): void { global $event_index; if ($event_index !== 6) throw new RuntimeException("missing receiver events"); }
process(value: -1);
process(value: -2);
process(value: -3);
verify_events();
