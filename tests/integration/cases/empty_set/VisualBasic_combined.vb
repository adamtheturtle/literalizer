Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New HashSet(Of Object)()
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New HashSet(Of Object)()
        }
    End Sub
End Module
