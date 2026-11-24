function consume_widget {}
$shared = @(
    1;
    2
)
$my_data = @(
    0
)
consume_widget $my_data
$my_data = $shared
consume_widget $my_data
