#cs
This script runs a series of GUI tests on the game_randomizer python package using AutoIT. 
It performs several basic tests to ensure the correct operation of the application.
The tests are conducted through simulated mouse clicks on the application's GUI, as the app doesn't have any button IDs
#ce

; Define the path to the Python environment and games file.
Local $executable = "D:\Python\Scripts\game_randomizer.exe"
; Set the test games list.
Local $parameter = "unit_tests"

; Set AutoIT options
Opt("MouseCoordMode", 0)

; Set up our button locations, because they don't have IDs
; $var =  [Button Name, X, Y]
Local $RollButton = ["Roll", 270, 480]
Local $SetupButton = ["Setup", 70, 580]
Local $PlayerCountOpen = ["Open Player Count", 340, 340]
Local $PlayerCountS1 = ["Set Player Count 2", 340, 360]
Local $PlayerCountS2 = ["Set Player Count 4", 340, 390]
Local $PizzazCheck = ["Pizzaz Checkbox",  260, 375]
Local $ExcludeCheck = ["Exclude Checkbox", 260, 400]
Local $AboutButton = ["About", 250, 580]
Local $CloseAboutButton = ["CloseAbout", 125, 220]
Local $ExitButton = ["Exit", 410, 580]

; Some simple functions
Func ButtonClick($bName, $time = 0)
	; Clicks a button based on the above dictionary of positions.
	MouseClick("left", $bName[1], $bName[2])
	; Log it to the console.
	Logger($bName[0] & ' button pressed.')
	Sleep($time)
EndFunc

Func StartApp()
	; Run the app
	Run(@ComSpec & " /c " & '"' & $executable & '" ' & $parameter, "", @SW_HIDE)
	; Wait 1 second for it to open.
	Sleep(1000)
EndFunc

Func Logger($msg)
	; Log info to the console.
	ConsoleWrite($msg & @CRLF)
EndFunc

; Run our tests

; Open and Close app.
StartApp()
ButtonClick($ExitButton)

; Open app, roll once, close.
StartApp()
ButtonClick($RollButton, 5000)
ButtonClick($RollButton, 5000)
ButtonClick($ExitButton)

; Open App, modify settings while periodically rolling.
StartApp()
ButtonClick($PlayerCountOpen, 1000)
ButtonClick($PlayerCountS2, 1000)
ButtonClick($PizzazCheck, 500)
ButtonClick($RollButton, 1000)
ButtonClick($RollButton, 1000)
ButtonClick($SetupButton, 1000)
ButtonClick($ExcludeCheck, 500)
ButtonClick($PlayerCountOpen, 1000)
ButtonClick($PlayerCountS1, 1000)
ButtonClick($RollButton, 1000)
ButtonClick($RollButton, 1000)
ButtonClick($RollButton, 1000)
ButtonClick($ExitButton)

; Open app, check the about page.
StartApp()
ButtonClick($AboutButton, 1000)
ButtonClick($CloseAboutButton, 1000)
ButtonClick($ExitButton)
