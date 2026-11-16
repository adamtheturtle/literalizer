<?php
$event_index = 0;
function observe_event(int $actual): void {
    global $event_index;
    $expected = [2, 0, 1, 1, 2, 101];
    if ($event_index >= 6 || $actual !== $expected[$event_index]) throw new RuntimeException("receiver event changed");
    $event_index++;
}
function make_widget(int $count): int { observe_event(1); observe_event($count); return $count + 100; }
function consume_widget(int $count): void { observe_event(2); observe_event($count); }
function verify_events(): void { global $event_index; if ($event_index !== 6) throw new RuntimeException("missing receiver events"); }
$my_data = 0;
consume_widget(count: $my_data);
$my_data = make_widget(count: 1);
consume_widget(count: $my_data);
verify_events();
