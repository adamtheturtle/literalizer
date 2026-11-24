<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [1, 42, 1, 42, 1, 142];
    if ($event_index >= 6 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function make_widget(int $count): int { observe_event(1); observe_event($count); return $count + 100; }
function verify_events(): void { global $event_index; if ($event_index !== 6) throw new RuntimeException("missing receiver events"); }
$my_data = 42;
make_widget(count: $my_data);
$my_data = make_widget(count: $my_data);
make_widget(count: $my_data);
verify_events();
