<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [1, 1];
    if ($event_index >= 2 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function process(int $data): int { observe_event(1); observe_event($data); return $data + 100; }
function verify_events(): void { global $event_index; if ($event_index !== 2) throw new RuntimeException("missing receiver events"); }
process(data: 1);
verify_events();
