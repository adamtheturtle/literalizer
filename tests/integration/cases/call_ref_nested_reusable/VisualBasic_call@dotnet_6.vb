Imports System.Collections.Generic
Module Check
    Function process(data As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = New Integer() {
            1,
            2
        }
        process(New Integer()() {item, item})
    End Sub
End Module
