with A_Stub; use A_Stub;
procedure Main is
    my_null : A_Val := ANull;
    my_data : A_Val := AList'[
        my_null,
        ANull
    ];
begin
    null;
end Main;
