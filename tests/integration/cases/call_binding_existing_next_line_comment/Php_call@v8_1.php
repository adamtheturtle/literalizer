<?php
function make_widget($count) {}
function consume_widget($count) {}
$my_data = make_widget(count: 42);
consume_widget(count: $my_data);
$my_data = make_widget(count: 42);
// note
consume_widget(count: $my_data);
