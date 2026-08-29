function process {}
$big_list = @(
    "x"
)
process @{"k" = $big_list} [ordered]@{"m" = $big_list}
