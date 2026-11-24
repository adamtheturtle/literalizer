with A_Stub; use A_Stub;
procedure Main is
    my_var : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := my_var;
begin
    null;
end Main;
