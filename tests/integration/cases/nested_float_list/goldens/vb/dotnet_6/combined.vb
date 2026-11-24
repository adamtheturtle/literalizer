Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Double()() {
            New Double() {1.5, 2.5},
            New Double() {3.5, 4.5}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Double()() {
            New Double() {1.5, 2.5},
            New Double() {3.5, 4.5}
        }
    End Sub
End Module
