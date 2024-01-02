#cs
This script runs a series of GUI tests on the game_randomizer python package using AutoIT. 
It performs several basic tests to ensure the correct operation of the application.
The tests are conducted through simulated mouse clicks on the application's GUI, as the app doesn't have any button IDs
#ce

; Define the path to the Python environment and games file.
Local $executable = "D:\Python\Scripts\game_randomizer.exe"


; Set AutoIT options
Opt("MouseCoordMode", 0)

; Set up our button locations, because they don't have IDs
; $var =  [Button Name, X, Y]
; Main Window
Local $RollButton = ["Roll", 270, 520]
Local $SetupButton = ["Setup", 70, 615]
Local $PlayerCountOpen = ["Open Player Count", 340, 340]
Local $PlayerCountS1 = ["Set Player Count 2", 340, 360]
Local $PlayerCountS2 = ["Set Player Count 4", 340, 390]
Local $PizzazCheck = ["Pizzaz Checkbox",  260, 375]
Local $ExcludeCheck = ["Exclude Checkbox", 260, 400]
Local $AboutButton = ["About", 250, 615]
Local $CloseAboutButton = ["CloseAbout", 125, 215]
Local $ExitButton = ["Exit", 410, 615]
; JSON Selector
Local $SelectJSON_ExitButton = ["Exit", 230, 170]
Local $SelectJSON_OpenDirButton = ["Open Directory", 220, 120]
Local $SelectJSON_Dropdown = ["JSON Dropdown", 220, 60]
Local $SelectJSON_DropdownUnitTest = ["Unit Tests", 220, 130]
Local $SelectJSON_Load = ["Load", 110, 170]

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
	Run(@ComSpec & " /c " & '"' & $executable & '"', "", @SW_HIDE)
	; Wait 1 second for it to open.
	Sleep(1000)
	; Select the window.
	WinActivate("Select Game List", "[CLASS:TkTopLevel]")
EndFunc

Func LoadJSON()
	; Open the app
	StartApp()
	; Select the window.
	WinActivate("Select Game List", "[CLASS:TkTopLevel]")
	; Click the dropdown menu.
	ButtonClick($SelectJSON_Dropdown)
	Sleep(100)
	; Select Unit Test from the list. 
	ButtonClick($SelectJSON_DropdownUnitTest)
	Sleep(100)
	; Load the unit test randomizer
	ButtonClick($SelectJSON_Load)
	; Select the new window.
	Sleep(500)
	WinActivate("Unit Tests Randomizer")
EndFunc

Func Logger($msg)
	; Log info to the console.
	ConsoleWrite($msg & @CRLF)
EndFunc

; Run our tests

; Open and Close app.
StartApp()
ButtonClick($SelectJSON_ExitButton)

; Open app, open asset folder, close asset folder, then exit.
StartApp()
ButtonClick($SelectJSON_OpenDirButton)
Sleep(2000)
If WinExists("[CLASS:CabinetWClass]") then
	Logger('Assets folder opened')
	WinActive("[CLASS:CabinetWClass]")
EndIf
WinClose("[CLASS:CabinetWClass]")
If not WinExists("[CLASS:CabinetWClass]") then
	Logger('Assets closed.')
EndIf
WinActivate("Select Game List", "[CLASS:TkTopLevel]")
ButtonClick($SelectJSON_ExitButton)

; Open app, roll once, close.
LoadJSON()
ButtonClick($RollButton, 5000)
ButtonClick($RollButton, 5000)
ButtonClick($ExitButton)

; Open App, modify settings while periodically rolling.
LoadJSON()
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
LoadJSON()
ButtonClick($AboutButton, 1000)
WinActivate("About", "[CLASS:TkTopLevel]")
ButtonClick($CloseAboutButton, 1000)
WinActivate("Unit Tests Randomizer")
ButtonClick($ExitButton)
