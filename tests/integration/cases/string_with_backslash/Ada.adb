procedure Check is
   my_data : A_Val := AList'(
       AStr ("C:\path\to\file"),
       AStr ("back\\slash"),
       AStr ("hello \""world\"""),
       AStr ("path\to ""# file"),
       AStr ("trailing\"),
       AStr ("both ""quotes''' here")
   );
begin
   null;
end Check;
