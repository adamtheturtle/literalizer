Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            Nothing,
            Nothing
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            Nothing,
            Nothing
        }
    End Sub
End Module
