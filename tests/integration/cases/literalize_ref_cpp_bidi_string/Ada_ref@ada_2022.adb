with A_Stub; use A_Stub;
procedure Main is
    text : A_Val := AStr ("a‪b");
    my_data : A_Val := AMap'[
        AEntry ("value", text)
    ];
begin
    null;
end Main;
