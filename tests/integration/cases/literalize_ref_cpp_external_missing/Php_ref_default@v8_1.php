<?php
function consume_widget($_arg) {}
$item = [
    1,
    2,
];
$my_data = [
    1,
    2,
];
consume_widget(_arg: $my_data);
$my_data = $item;
consume_widget(_arg: $my_data);
