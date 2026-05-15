with A_Stub; use A_Stub;
procedure Main is
    shared_var : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AList'[
        shared_var,
        shared_var
    ];
begin
    null;
end Main;
