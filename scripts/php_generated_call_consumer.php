<?php

$rows = [];

function collect(string $tag, mixed $payload): void {
    global $rows;
    $rows[] = [$tag, $payload];
}
