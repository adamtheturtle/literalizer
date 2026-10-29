with A_Stub; use A_Stub;
procedure Main is
    shared : A_Val := AStr ("s");
    my_data : A_Val := AMap'[
        AEntry ("value", shared)
    ];
begin
    null;
end Main;
