Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim UntypedValue = New Object() {}
        process(New Object() {UntypedValue, UntypedValue})
    End Sub
End Module
