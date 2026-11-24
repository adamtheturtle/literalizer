<?php
$my_data = [
    "ancient_date" => "1500-03-01",
    "modern_date" => "2024-01-15",
    "before_date" => "1582-10-04",
    "gap_date" => "1582-10-10",
    "transition_date" => "1582-10-15",
    "after_date" => "1582-10-16",
    "before_naive" => new DateTime("1582-10-04T12:30:00.000001", new DateTimeZone("UTC")),
    "gap_naive" => new DateTime("1582-10-10T12:30:00.500000", new DateTimeZone("UTC")),
    "transition_positive" => new DateTime("1582-10-15T00:30:00+18:00"),
    "transition_negative" => new DateTime("1582-10-15T23:30:00-18:00"),
    "after_positive" => new DateTime("1582-10-16T00:30:00+18:00"),
];
