!include "MUI2.nsh"
!include "LogicLib.nsh"
Unicode true
CRCCheck on
ManifestSupportedOS all
XPStyle on
Name "MusicDL"
OutFile "music_dl_0.3_setup.exe"
InstallDir "$PROGRAMFILES\musicDL"
InstallDirRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "InstallLocation"
RequestExecutionLevel admin
SetCompress auto
SetCompressor /solid lzma
SetDatablockOptimize on
VIAddVersionKey ProductName "MusicDL"
VIAddVersionKey LegalCopyright "Copyright 2018 Manuel Cortéz."
VIAddVersionKey ProductVersion "0.3"
VIAddVersionKey FileVersion "0.3"
VIProductVersion "0.3.0.0"
VIFileVersion "0.3.0.0"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
var StartMenuFolder
!insertmacro MUI_PAGE_STARTMENU startmenu $StartMenuFolder
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_LINK "Visit MusicDL website"
!define MUI_FINISHPAGE_LINK_LOCATION "https://manuelcortez.net/music_dl"
!define MUI_FINISHPAGE_RUN "$INSTDIR\musicDL.exe"
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Spanish"
!insertmacro MUI_LANGUAGE "Russian"
!insertmacro MUI_RESERVEFILE_LANGDLL
Section
SetShellVarContext All
SetOutPath "$INSTDIR"
File /r dist\main\*
CreateShortCut "$DESKTOP\musicDL.lnk" "$INSTDIR\musicDL.exe"
!insertmacro MUI_STARTMENU_WRITE_BEGIN startmenu
CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
CreateShortCut "$SMPROGRAMS\$StartMenuFolder\MusicDL.lnk" "$INSTDIR\musicDL.exe"
CreateShortCut "$SMPROGRAMS\$StartMenuFolder\MusicDL on the web.lnk" "http://manuelcortez.net/music_dl"
CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
!insertmacro MUI_STARTMENU_WRITE_END
WriteUninstaller "$INSTDIR\Uninstall.exe"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "DisplayName" "MusicDL"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "UninstallString" '"$INSTDIR\uninstall.exe"'
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall" "InstallLocation" $INSTDIR
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall" "Publisher" "Manuel Cortéz"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "DisplayVersion" "0.3"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "URLInfoAbout" "https://manuelcortez.net/music_dl"
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "VersionMajor" 0
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "VersionMinor" 1
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "NoModify" 1
WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL" "NoRepair" 1
SectionEnd
Section "Uninstall"
SetShellVarContext All
DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\musicDL"
RMDir /r /REBOOTOK $INSTDIR
Delete "$DESKTOP\MusicDL.lnk"
!insertmacro MUI_STARTMENU_GETFOLDER startmenu $StartMenuFolder
RMDir /r "$SMPROGRAMS\$StartMenuFolder"
SectionEnd
Function .onInit
!insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd
