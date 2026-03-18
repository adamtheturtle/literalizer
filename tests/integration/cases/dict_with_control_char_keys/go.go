package main

var _ = map[string]any{
    "key\nwith\nnewlines": "value1",
    "key	with	tabs": "value2",
}
