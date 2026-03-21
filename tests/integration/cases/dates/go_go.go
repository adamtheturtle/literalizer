package main

import "time"

var _ = map[string]any{
    "date": time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC),
    "datetime": time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC),
}
