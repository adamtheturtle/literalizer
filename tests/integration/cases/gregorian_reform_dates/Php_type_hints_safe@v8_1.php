<?php
$my_data = [
    "ancient_date" => new DateTime("1500-03-01", new DateTimeZone("UTC")),
    "modern_date" => new DateTime("2024-01-15", new DateTimeZone("UTC")),
    "before_date" => new DateTime("1582-10-04", new DateTimeZone("UTC")),
    "gap_date" => new DateTime("1582-10-10", new DateTimeZone("UTC")),
    "transition_date" => new DateTime("1582-10-15", new DateTimeZone("UTC")),
    "after_date" => new DateTime("1582-10-16", new DateTimeZone("UTC")),
    "before_naive" => new DateTime("1582-10-04T12:30:00.000001", new DateTimeZone("UTC")),
    "gap_naive" => new DateTime("1582-10-10T12:30:00.500000", new DateTimeZone("UTC")),
    "transition_positive" => new DateTime("1582-10-15T00:30:00+18:00"),
    "transition_negative" => new DateTime("1582-10-15T23:30:00-18:00"),
    "after_positive" => new DateTime("1582-10-16T00:30:00+18:00"),
];
