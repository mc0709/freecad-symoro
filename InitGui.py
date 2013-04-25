
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012 Gael Ecorchard <galou_breizh@yahoo.fr>             * 
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__="FreeCAD Symoro+ Workbench - InitGui file"
__author__ = "Gael Ecorchard <galou_breizh@yahoo.fr>"
__url__ = ["http://free-cad.sourceforge.net"]

import os

class SymoroWorkbench(Workbench):
    "The Symoro Workbench"
    # TODO: change icon
    Icon = """
        /* XPM */
        static char * draft_xpm[] = {
        "14 16 96 2",
        "       c None",
        ".      c #584605",
        "+      c #513E03",
        "@      c #E6B50D",
        "#      c #C29F0E",
        "$      c #6E5004",
        "%      c #F7BD0B",
        "&      c #8F7008",
        "*      c #F3C711",
        "=      c #B1950F",
        "-      c #785402",
        ";      c #946C05",
        ">      c #FABF0B",
        ",      c #F7C20E",
        "'      c #8D740A",
        ")      c #F8D115",
        "!      c #9F8A0F",
        "~      c #593D00",
        "{      c #FEB304",
        "]      c #F3B208",
        "^      c #987407",
        "/      c #FDC70E",
        "(      c #EFC311",
        "_      c #8F790C",
        ":      c #FBDA18",
        "<      c #8B7C0F",
        "[      c #B88203",
        "}      c #FEBA08",
        "|      c #E7B00A",
        "1      c #A17E09",
        "2      c #FCCE12",
        "3      c #E6C213",
        "4      c #96830E",
        "5      c #FBE11C",
        "6      c #786F0F",
        "7      c #CA9406",
        "8      c #FDC10B",
        "9      c #D8AA0C",
        "0      c #AE8E0C",
        "a      c #FCD415",
        "b      c #DBBF15",
        "c      c #A09012",
        "d      c #F9E61F",
        "e      c #69650E",
        "f      c #4B3702",
        "g      c #DAA609",
        "h      c #CAA50E",
        "i      c #BB9D10",
        "j      c #FCDB18",
        "k      c #CEB817",
        "l      c #AB9E15",
        "m      c #F2E821",
        "n      c #5E5C0E",
        "o      c #503D03",
        "p      c #E8B60D",
        "q      c #CAAF13",
        "r      c #C1B218",
        "s      c #B6AE19",
        "t      c #EAE625",
        "u      c #575723",
        "v      c #594605",
        "w      c #F1C511",
        "x      c #AB9510",
        "y      c #D7C018",
        "z      c #FBE81F",
        "A      c #B3AC18",
        "B      c #BCB81D",
        "C      c #7F8051",
        "D      c #645207",
        "E      c #9D8C11",
        "F      c #E4D31C",
        "G      c #BEB62F",
        "H      c #6C6A3F",
        "I      c #E1E1E1",
        "J      c #73610A",
        "K      c #7C720F",
        "L      c #A1A084",
        "M      c #FFFFFF",
        "N      c #565656",
        "O      c #887921",
        "P      c #988F44",
        "Q      c #BFBEB7",
        "R      c #EEEEEC",
        "S      c #C0C0C0",
        "T      c #323232",
        "U      c #4D4B39",
        "V      c #C7C7C7",
        "W      c #FBFBFB",
        "X      c #BFBFBF",
        "Y      c #141414",
        "Z      c #222222",
        "`      c #303030",
        " .     c #313131",
        "..     c #282828",
        "+.     c #121212",
        "@.     c #000000",
        "        .                   ",
        "      + @ #                 ",
        "    $ % & * =             X ",
        "  - ; > , ' ) !           X ",
        "~ { ] ^ / ( _ : <         X ",
        "  [ } | 1 2 3 4 5 6       X ",
        "    7 8 9 0 a b c d e     X ",
        "    f g / h i j k l m n   X ",
        "      o p 2 i q 5 r s t u X ",
        "        v w a x y z A B C X ",
        "          D ) j E F G H I X ",
        "            J : 5 K L M M X ",
        "              O P Q R M S X ",
        "  X X X X X X X X X X X X X ",
        "                    `  ...+.",
        "    @.@.@.@.@.@.@.@.        "};
        """

    MenuText = "Symoro"
    ToolTip = "The Symoro module is used for robot modeling"

    def Initialize(self):
        import importSymoro
        #importSymoro.createGeometry()
                                        
    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def ContextMenu(self, recipient):
        pass

    def GetClassName(self): 
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(SymoroWorkbench)
#App.addExportType("Open CAD Format (*.oca)","importOCA")

