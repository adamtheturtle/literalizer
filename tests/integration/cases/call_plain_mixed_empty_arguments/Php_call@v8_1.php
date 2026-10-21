<?php
function make_widget($before, $populated, $after) {}
make_widget(before: [], populated: [1], after: []);
make_widget(before: ["text"], populated: [2], after: []);
make_widget(before: [], populated: ["text"], after: []);
make_widget(before: ["text"], populated: [2], after: [3]);
