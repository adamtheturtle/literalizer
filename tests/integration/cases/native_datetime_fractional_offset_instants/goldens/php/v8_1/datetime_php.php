<?php
$my_data = [
    "stamps" => [new DateTime("2001-02-03T04:05:06.123456+00:00"), new DateTime("2001-02-03T04:05:06.123456+00:00:01"), new DateTime("2001-02-03T04:05:06.123456-00:00:01"), new DateTime("2001-02-03T04:05:06.123455+00:00"), new DateTime("2001-02-03T04:05:06.123457+00:00"), new DateTime("2001-02-03T04:05:05.623456+00:00"), new DateTime("2001-02-03T04:05:06.623456+00:00"), new DateTime("2001-02-02T22:34:51.123455+00:00"), new DateTime("2001-02-03T09:35:21.123457+00:00"), new DateTime("2001-02-02T04:05:06.123457+00:00"), new DateTime("2001-02-04T04:05:06.123455+00:00")],
];
$expected = [981173106123456, 981173105123456, 981173107123456, 981173106123455, 981173106123457, 981173105623456, 981173106623456, 981153291123455, 981192921123457, 981086706123457, 981259506123455];
foreach ($my_data["stamps"] as $index => $stamp) {
    $actual = (int) $stamp->format("U") * 1000000 + (int) $stamp->format("u");
    if ($actual !== $expected[$index]) {
        throw new RuntimeException("UTC instant changed at index " . $index);
    }
}
// Whole-second offsets remain representable; fractional offsets normalize to UTC.
$offsets = [0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0];
foreach ($my_data["stamps"] as $index => $stamp) {
    if ($stamp->getOffset() !== $offsets[$index]) {
        throw new RuntimeException("UTC offset changed at index " . $index);
    }
}
