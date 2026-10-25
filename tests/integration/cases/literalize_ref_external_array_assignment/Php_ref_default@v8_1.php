<?php
function consume_widget($arg_value) {}
$shared = [
    1,
    2,
];
$my_data = [
    0,
];
consume_widget(arg_value: $my_data);
$my_data = $shared;
consume_widget(arg_value: $my_data);
