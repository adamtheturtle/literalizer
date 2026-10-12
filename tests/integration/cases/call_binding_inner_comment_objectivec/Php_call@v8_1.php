<?php
function make_widget($count) {}
$my_data = make_widget(count: 42) ?
make_widget(count: 42) // inner
: nil // trailing;
