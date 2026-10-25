<?php
function make_widget($count) {}
function consume_widget($count) {}
$my_data = make_widget(count: 0);
consume_widget(count: $my_data);
$my_data = make_widget(count: 1);
consume_widget(count: $my_data);
