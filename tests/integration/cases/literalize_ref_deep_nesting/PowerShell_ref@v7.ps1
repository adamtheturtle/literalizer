$Deep = @(
    ,@(
        "one";
        "two"
    );
    ,@(
        "three";
        "four"
    )
)
$my_data = @{
    "a" = @{
        "b" = @{
            "c" = $Deep
        }
    }
}
