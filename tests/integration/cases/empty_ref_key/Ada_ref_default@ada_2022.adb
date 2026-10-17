with A_Stub; use A_Stub;
procedure Main is
    external_value : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AList'[
        external_value
    ];
begin
    null;
end Main;
