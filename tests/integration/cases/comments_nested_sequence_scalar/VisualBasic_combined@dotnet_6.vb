Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String()() {
            New String() {"ADD", "alice", "hello"},
            New String() {
                "DEL",
                "bob",
                "5"  ' removes "world"
            }
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String()() {
            New String() {"ADD", "alice", "hello"},
            New String() {
                "DEL",
                "bob",
                "5"  ' removes "world"
            }
        }
    End Sub
End Module
