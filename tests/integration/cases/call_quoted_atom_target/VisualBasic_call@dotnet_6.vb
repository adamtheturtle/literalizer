Imports System.Collections.Generic
Module Check
    Function DoThing(x As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        DoThing(1)
        DoThing(2)
    End Sub
End Module
