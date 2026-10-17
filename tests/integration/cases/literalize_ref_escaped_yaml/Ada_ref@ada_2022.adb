with A_Stub; use A_Stub;
procedure Main is
    existing : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := existing;
begin
    null;
end Main;
