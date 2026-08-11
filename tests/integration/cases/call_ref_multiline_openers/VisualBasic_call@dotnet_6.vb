Imports System.Collections.Generic
Module Check
    Function consume(items As Object, mapping As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim foo = 42
        consume(New Object() {
            New Dictionary(Of String, Object) From {
                {"other", 1}
            },
            foo
        }, New Dictionary(Of String, Object) From {
            {"left", foo},
            {"other", 1}
        })
    End Sub
End Module
