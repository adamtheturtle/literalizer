with A_Stub; use A_Stub;
procedure Main is
    val_x : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    val_y : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AList'[
        val_x,
        val_y
    ];
begin
    null;
end Main;
