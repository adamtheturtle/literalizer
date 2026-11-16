<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [1, 42, 2, 142];
    if ($event_index >= 4 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function make_widget(int $value): int { observe_event(1); observe_event($value); return $value + 100; }
function consume(int $value): void { observe_event(2); observe_event($value); }
function verify_events(): void { global $event_index; if ($event_index !== 4) throw new RuntimeException("missing receiver events"); }
$my_data = make_widget(value: 42);
consume(value: $my_data);
verify_events();
