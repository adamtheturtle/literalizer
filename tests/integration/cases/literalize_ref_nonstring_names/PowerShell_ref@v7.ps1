$Actual = @{
    "_" = "_"
}
$my_data = @(
    @{"`$ref" = 1};
    @{"`$ref" = $null};
    $Actual
)
