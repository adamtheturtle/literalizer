<?php
function consume($value) { echo json_encode(["is_list" => array_is_list($value), "first_key_type" => is_null(array_key_first($value)) ? null : gettype(array_key_first($value)), "encoded_value" => json_encode($value)]); }
consume(value: []);