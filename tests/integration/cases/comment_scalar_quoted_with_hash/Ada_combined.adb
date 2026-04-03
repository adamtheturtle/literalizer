procedure Check is
   procedure Check_Declaration is
      my_data : A_Val := AStr ("hello # world"  -- note);
   begin
      null;
   end Check_Declaration;
   procedure Check_Assignment is
   begin
      my_data := AStr ("hello # world"  -- note);
   end Check_Assignment;
begin
   null;
end Check;
