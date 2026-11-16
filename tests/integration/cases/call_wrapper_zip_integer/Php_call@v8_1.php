<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [1, 1, 2, 101, 3, 42];
    if ($event_index >= 6 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function process(int $value): int { observe_event(1); observe_event($value); return $value + 100; }
function emit(int $actual, int $zipped): void { observe_event(2); observe_event($actual); observe_event(3); observe_event($zipped); }
function verify_events(): void { global $event_index; if ($event_index !== 6) throw new RuntimeException("missing receiver events"); }
emit(process(value: 1), 42);
verify_events();
