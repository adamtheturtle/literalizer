<?php
function capture($nan_value, $positive_infinity, $negative_infinity, $finite_value, $date_value, $datetime_value, $text_value) {}
capture(nan_value: NAN, positive_infinity: INF, negative_infinity: -INF, finite_value: 1.25, date_value: new DateTime("2024-01-15", new DateTimeZone("UTC")), datetime_value: new DateTime("2024-01-15T12:34:56", new DateTimeZone("UTC")), text_value: "[ordinary text]");
