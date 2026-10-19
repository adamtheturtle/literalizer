$Actual = 42
$my_data = @(
    @{"`$ref" = 1};
    @{"`$ref" = $null};
    $Actual
)
