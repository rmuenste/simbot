import datetime

current_date = datetime.datetime.now()
date_string_short = current_date.strftime("%m/%d/%y") 

SYSTEM_STRING1 = """
You are a master of smalltalk, it is a delight for everyone to chat with you.
"""

SYSTEM_STRING2 = """
You are a translator to German, you translate all input given to you to the German language.
"""

SYSTEM_STRING3 = """
You are a helpful assistant for creating configuration files
"""

REDUCED_EXPLANATION_STRING =f"""
[SigmaFileInfo]
FileType=ToExtrud3D <Internal parameter identifying the file type>
FileVersion=SIGMA 10.0 <Internal version parameter>
Date={date_string_short} <The current date>
SigmaVersion=SIGMA 12.0.1(4492) <Internal version of SIGMA used>
ConfigId=XY60_PE_400.xpro-201907020948 <Internal system job ID>
[E3DGeometryData]
[E3DGeometryData/Machine]
Type=TSE,SSE,DIE <Extruder type>
Unit=mm <Unit for input parameters>
Zwickel=straight,curved <Barrel shape; can be straight or curved>
MachineName=XY 60 <Extruder name>
RotationDirection=LEFT,RIGHT <Extruder rotation direction: LEFT (default) or RIGHT>
BarrelDiameter=51.5 <Barrel diameter (default: 2 * screw diameter + 2 * screw clearance)> [mm]
CenterlineDistance=41.5 <Centerline distance between axes, required for TSE simulations> [mm]
BarrelStraightCut=0.4 <Depth of the V-cut (default: 2.5 percent of BarrelDiameter, used only for twin screws)> [mm]
NoOfElements=1 <Number of elements in the extruder>
NoOfFlights=1 <Number of flights in the extruder>
BarrelLength=70.0 <Length of the barrel/housing> [mm]
"""

EXPLANATION_STRING = """
[SigmaFileInfo]
FileType=ToExtrud3D <Internal parameter identifying the file type>
FileVersion=SIGMA 10.0 <Internal version parameter>
Date=07/02/19 <The current date>
SigmaVersion=SIGMA 12.0.1(4492) <Internal version of SIGMA used>
ConfigId=XY60_PE_400.xpro-201907020948 <Internal system job ID>

[E3DGeometryData]
[E3DGeometryData/Machine]
Type=TSE,SSE,DIE <Extruder type>
Unit=mm <Unit for input parameters>
Zwickel=straight,curved <Barrel shape; can be straight or curved>
MachineName=XY 60 <Extruder name>
RotationDirection=LEFT,RIGHT <Extruder rotation direction: LEFT (default) or RIGHT>
BarrelDiameter=51.5 <Barrel diameter (default: 2 * screw diameter + 2 * screw clearance)> [mm]
CenterlineDistance=41.5 <Centerline distance between axes, required for TSE simulations> [mm]
BarrelStraightCut=0.4 <Depth of the V-cut (default: 2.5 percent of BarrelDiameter, used only for twin screws)> [mm]
NoOfElements=1 <Number of elements in the extruder>
NoOfFlights=1 <Number of flights in the extruder>
BarrelLength=70.0 <Length of the barrel/housing> [mm]

[E3DGeometryData/Machine/Element_1]
GapScrewScrew=0.7 <Clearance between screws in a twin-screw extruder> [mm]
ObjectType=screw <The object is a screw>
Unit=mm <Unit for input parameters>
startposition = 0.0 <Starting position of the screw> [mm]
off_filelist = screw_extended_by_10.off <File containing the 3D geometry of the screw>
off_filelistL = screw_+Y_extended_by_10.off <File for the left-hand side of the screw geometry>
off_filelistR = screw_-Y_extended_by_10.off <File for the right-hand side of the screw geometry>
innerdiameter = 30.9 <Inner diameter of the screw> [mm]
type = OFF,OFF_LR <Type of input geometry; OFF requires `off_filelist`, OFF_LR requires both `off_filelistL` and `off_filelistR`>

[E3DProcessParameters]
ScrewSpeed=300.0 <Rotational speed of the screw> [rpm]
ProcessType=THROUGHPUT <Type of process: mass throughput>
MassThroughput=300.0 <Mass of material processed per hour> [kg/h]
MaterialTemperature=290.0 <Inflow temperature of the material and starting melt temperature> [C deg]
BarrelTemperature=280.0 <Barrel temperature (used if not adiabatic)> [C deg]
ScrewTemperature=_INVALID_ <Screw temperature (used if not adiabatic)> [C deg]
BarrelTemperatureAdiabatic=YES,NO <If NO, a specific ScrewTemperature must be defined>
ScrewTemperatureAdiabatic=YES,NO <If NO, a specific BarrelTemperature must be defined>

[E3DProcessParameters/Material]
Name=PC1 <Name of the material>
Type=Polymer <Type of material>

[E3DProcessParameters/Material/RheologicalData]
CalcVisco=Carreau <Viscosity model used for the material>
CalcTemp=TbTs <Temperature model used for the material>

[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=397.69 <Viscosity at zero shear rate> [Pa.s]
RecipVelocity=0.00029 <Reciprocal of the characteristic shear rate velocity> [s]
Exponent=0.92012 <Exponent in the Carreau viscosity model> [unitless]

[E3DProcessParameters/Material/RheologicalData/TBTS]
standardtemperature = 135.7 <Standard processing temperature> [C deg]
referencetemperature = 300.0 <Reference temperature for rheological calculations> [C deg]

[E3DProcessParameters/Material/ThermoData]
heatconductivity = 0.134 <Thermal conductivity of the material> [W/m/K]
heatconductivityslope = 0.0 <Slope of the thermal conductivity with respect to temperature>
heatcapacity = 1.75 <Specific heat capacity of the material> [kJ/kg/K]
heatcapacityslope = 0.0 <Slope of the heat capacity with respect to temperature>
densitymodel = DENSITY <Density model used for the material>

[E3DProcessParameters/Material/ThermoData/Density]
Density=1.0 <Density of the melt> [g/cm3]
DensitySlope=0.0 <Slope of the density with respect to temperature>

[E3DSimulationsettings]
MeshQuality=coarse, medium, fine <Mesh resolution>
HexMesher=TwinScrew / HollowCylinder <Mesh generator type: TwinScrew or HollowCylinder>
KTPRelease=NO <Flag indicating whether KTP release is activated>
"""

#BEHAVIOR_STRING= f"""
#You are an assistant for creating INI file. You can take this INI file as a template:
#[SigmaFileInfo] FileType=ToExtrud3D FileVersion=SIGMA 10.0 Date={date_string_short} SigmaVersion=SIGMA 12.0.1(4492) ConfigId=XY60_PE_400.xpro-201907020948 [E3DGeometryData] [E3DGeometryData/Machine] Type=TSE Unit=mm Zwickel=straight MachineName=XY 60 RotationDirection=LEFT BarrelDiameter=51.5 CenterlineDistance=41.5 BarrelStraightCut=0.4 NoOfElements=1 NoOfFlights=1 BarrelLength=41.0 [E3DGeometryData/Machine/Element_1] GapScrewScrew=0.7 ObjectType=screw Unit=mm startposition=0.0 off_filelistL=screw_-Y_extended_by_10.off off_filelistR=screw_+Y_extended_by_10.off innerdiameter=30.9 type=OFF_LR [E3DProcessParameters] ScrewSpeed=400.0 ProcessType=THROUGHPUT MassThroughput=300.0 MaterialTemperature=285.0 BarrelTemperature=270.0 ScrewTemperature=_INVALID_ BarrelTemperatureAdiabatic=NO ScrewTemperatureAdiabatic=YES [E3DProcessParameters/Material] Name=PET1 Type=Polymer [E3DProcessParameters/Material/RheologicalData] CalcVisco=Carreau CalcTemp=TbTs [E3DProcessParameters/Material/RheologicalData/Carreau] ZeroViscosity=173.15 RecipVelocity=0.002 Exponent=0.04931 [E3DProcessParameters/Material/RheologicalData/TBTS] standardtemperature=125.0 referencetemperature=285.0 [E3DProcessParameters/Material/ThermoData] heatconductivity=0.22 heatconductivityslope=0.0 heatcapacity=1.93 heatcapacityslope=0.0 densitymodel=DENSITY [E3DProcessParameters/Material/ThermoData/Density] Density=1.18 DensitySlope=0.0 [E3DSimulationsettings] MeshQuality=medium HexMesher=TwinScrew KTPRelease=NO
#A user may now send a message in which he defines one or more key value pairs. Your task is to find and replace the values in the template by the value(s) given in user's message. Your reply always includes the full, updated INI file. A user may enter keys in the German language if so try to find the matching key and replace its value.
#A user may also ask questions about the key-values in the INI file. If you identify a users message as a question about the meaning of a key-value pair in the INI file, try to explain it based on the following info : {EXPLANATION_STRING}.
#I have put the information in angled brackets after the key-value pairs. If you find no angled backets after the key-value pairs try to explain based on your world knowledge.
#"""

BEHAVIOR_STRING= f"""
You are an assistant for creating INI file. You can take this INI file as a template: {EXPLANATION_STRING}
This is an INI file enriched with information about the key-value pairs which is inside the angled brackets. In square brackets I have the standard units for the values (if applicable).
A user may now send a message in which he defines one or more key value pairs. Your task is to find and replace the values in the template by the value(s) given in user's message, do not replace values not mentioned by the user. If you
find in the chat history a previous reply with a full INI file then update values in this file instead of the template INI file. 
Your reply always includes the full(every section), updated INI file without the extra information in angled or square brackets. A user may enter keys in the German language if so try to find the matching key and replace its value.
A user may also ask questions about the key-values in the INI file. If you identify a users message as a question about the meaning of a key-value pair in the INI file, try to explain it 
based on the information provided in the angled brackets after the particular key-value pair. If you find no angled backets after the key-value pairs try to explain based on your world knowledge.
"""

REDUCED_BEHAVIOR_STRING= f"""
You are an assistant for creating INI file. You can take this INI file as a template: {REDUCED_EXPLANATION_STRING}
This is an INI file enriched with information about the key-value pairs which is inside the angled brackets. In square brackets I have the standard units for the values (if applicable).
A user may now send a message in which he defines one or more key value pairs. Your task is to find and replace the values in the template by the value(s) given in user's message, do not replace values not mentioned by the user. If you
find in the chat history a previous reply with a full INI file then update values in this file instead of the template INI file. 
Your reply always includes the full(every section), updated INI file without the extra information in angled or square brackets. A user may enter keys in the German language if so try to find the matching key and replace its value.
A user may also ask questions about the key-values in the INI file. If you identify a users message as a question about the meaning of a key-value pair in the INI file, try to explain it 
based on the information provided in the angled brackets after the particular key-value pair. If you find no angled backets after the key-value pairs try to explain based on your world knowledge.
"""

BEHAVIOR_STRING2= f"""
You are an assistant for creating INI file. You can take this INI file as a template: {REDUCED_EXPLANATION_STRING}
This is an INI file enriched with information about the key-value pairs which is inside the angled brackets. In square brackets I have the standard units for the values (if applicable).
A user may now send a message in which he defines one or more key value pairs. Your task is to find and replace the values in the INI file returned by the tool get_current_state by the value(s) given in user's message. If you
Once you are done replacing call the update_state tool with the new INI file as a string parameter. Your reply will be the return value of the update_state tool which is the INI updated with the last user input. A user may enter keys in the German language if so try to find the matching key and replace its value.
A user may also ask questions about the key-values in the INI file. If you identify a users message as a question about the meaning of a key-value pair in the INI file, try to explain it 
based on the information provided in the angled brackets after the particular key-value pair. If you find no angled backets after the key-value pairs try to explain based on your world knowledge.
"""


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

georeader = """
"FOERD", "THREADED": StartPosition, ElementLength, Lead, Diameter, GapScrewScrew, KindOfConveying
"KNET", "KNEADING": StartPosition, Diameter, GapScrewScrew, DiscWidth, StaggeringAngle, KneadingDiscs, KindOfkneading
"TKNET", "TRUEKNEADING": StartPosition, Diameter, GapScrewScrew, DiscFrac, DiscWidth, StaggeringAngle, KneadingDiscs, KindOfkneading
"SKNET", "SHOULDEREDKNEADING": StartPosition, Diameter, GapScrewScrew, DiscWidth, StaggeringAngle, KneadingDiscs, KindOfkneading
"SME", "SCREWMIXING": StartPosition, ElementLength, Lead, Diameter, GapScrewScrew, KindOfConveying, NoOfGrooves, KindOfGrooves, GroovesDepth, GroovesWidth, GroovesLead
"ZME", "TOOTHMIXING": StartPosition, NoOfRows, DiscWidth, DiscDiscGap, DiscShellGap, InnerDiameter, NoOfTeeth, KindOfGrooves, GroovesDepth, GroovesWidth, GroovesLead
"""

EXPLANATION_STRING_OM = f"""
[SigmaFileInfo]
FileType=ToExtrud3D <Internal parameter to identify the file>
FileVersion=SIGMA 10.0 <Internal version parameter>
Date=07/02/19 <The current date>
SigmaVersion=SIGMA 12.0.1(4492) <The internal version of SIGMA used>
ConfigId=XY60_PE_400.xpro-201907020948 <The system internal job id>

[E3DGeometryData]
[E3DGeometryData/Machine]
Type=TSE,SSE,DIE <The extruder type can be TSE (twinscrew extruder), SSE (singlescrew extruder), DIE (die extruder)>
Unit=mm <Unit to be used for the input parameters>
Zwickel=straight,curved <A parameter describing the barrel shape. Can be straight or curved>
MachineName=XY 60 <The name of the extruder>
RotationDirection=LEFT,RIGHT <Rotation direction of the extruder can be LEFT (default) or RIGHT>
BarrelDiameter=51.5 <The diameter of the barrel (default value: 2*screw diameter + 2*screw clearance)> [mm]
CenterlineDistance=41.5 <The centerline distance between the axes, mandatory for TSE sims> [mm]
BarrelStraightCut=0.4 <The depth of the V-cut (default 2.5 percent of the BarrelDiameter, used only for twinscrews)> [mm]
NoOfElements=1 <The number of elements of the extruder>
NoOfFlights=1 <The number of flights of the extruder>
BarrelLength=70.0 <The length of the barrel/housing> [mm]

[E3DGeometryData/Machine/Element_1]
GapScrewScrew=0.7 <Try to describe with your world knowledge> [mm]
ObjectType=screw <Try to describe with your world knowledge>
Unit=mm <Try to describe with your world knowledge>
startposition = 0.0 <Try to describe with your world knowledge> [mm]
off_filelist = screw_extended_by_10.off
off_filelistL = screw_+Y_extended_by_10.off
off_filelistR = screw_-Y_extended_by_10.off
innerdiameter = 30.9 <Try to describe with your world knowledge> [mm]
type=FOERD,KNET,SKNET,TKNET,SME,ZME,OFF,OFF_LR <type of screw definition>
the "TYPE" keyword value is a more complex one and needs to be carefully assigned. there are 2 main cases to decide, if the screw is defined via a surface triangulation (*.off files are provided) or analytically (FOERD,KNET,SKNET,TKNET,SME,ZME)
Now, in case that we do have an screw definition via OFF files:
type = OFF,OFF_LR | if OFF then off_filelist has to be defined, if OFF_LR then both off_filelistL and off_filelistR has to be defined | <The type of the input geometry (here a .off file)>
in case that we do have an analytical screw definition there are additional parameters applying for a complete definition of the segment, imporant is that all these additional parameters have to be provided for the unique definition of the screw:
type = FOERD,KNET,SKNET,TKNET,SME,ZME (the respective geometrical parameter keywords for these screw types are inhere:
{georeader}

[E3DProcessParameters]
ScrewSpeed=300.0 <Try to describe with your world knowledge> [rpm <==> round per minute]
ProcessType=THROUGHPUT
MassThroughput=300.0 <Try to describe with your world knowledge> [kg/h]
MaterialTemperature=290.0 <inflow temeprtature of the material into the extruder. is also used as the start temperature of the melt> [C deg]
BarrelTemperature=280.0 <temperature of the barrel, in case that it is not set to adiabatic> [C deg]
ScrewTemperature=_INVALID_ <temperature of the screw, in case that it is not set to adiabatic> [C deg]
BarrelTemperatureAdiabatic=YES,NO  if NO ScrewTemperature has to be defined by a temperature value
ScrewTemperatureAdiabatic=YES,NO if NO BarrelTemperature has to be defined by a temperature value

[E3DProcessParameters/Material]
Name=PC1
Type=Polymer

[E3DProcessParameters/Material/RheologicalData]
CalcVisco=Carreau <Try to describe with your world knowledge>
CalcTemp=TbTs

[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=397.69 <Try to describe with your world knowledge> [Pa.s]
RecipVelocity= 0.00029 <Try to describe with your world knowledge> [s]
Exponent=0.92012 <Try to describe with your world knowledge> [unitless]

[E3DProcessParameters/Material/RheologicalData/TBTS]
standardtemperature = 135.7 <Try to describe with your world knowledge> [C deg]
referencetemperature = 300.0 <Try to describe with your world knowledge> [C deg]

[E3DProcessParameters/Material/ThermoData]
heatconductivity = 0.134 <Try to describe with your world knowledge> [W/m/K]
heatconductivityslope = 0.0
heatcapacity = 1.75 <Try to describe with your world knowledge> [kJ/kg/K]
heatcapacityslope = 0.0
densitymodel = DENSITY

[E3DProcessParameters/Material/ThermoData/Density]
Density=1.0 <density of the melt> [g/cm3]
DensitySlope=0.0

[E3DSimulationsettings]
MeshQuality=coarse, medium, fine <resolution of the mesh>
HexMesher=TwinScrew / HollowCylinder <types of the mesh generators>
KTPRelease=NO
"""

OUT3 = """

[SigmaFileInfo]
FileType=ToExtrud3D
FileVersion=SIGMA 10.0
Date=01/09/18
SigmaVersion=SIGMA 11.0.3(4229)
[E3DGeometryData]
[E3DGeometryData/Machine]
Unit=cm
Type=TSE
BarrelCut=straight
MachineName=ZSK25
RotationDirection=RIGHT
BarrelDiameter=25.3
CenterlineDistance=21.1
BarrelStraightCut=0.4
NoOfElements=1
NoOfFlights=2
BarrelLength=22

[E3DGeometryData/Machine/Element_1]
ObjectType=screw
Unit=cm
Type=THREADED
GapScrewScrew=0.4
Name=36/36
ElementLength=16.00000000
Diameter=25.00000000
StartPosition=2.0
Lead=36.0
KindOfConveying=CONVEYING

[E3DProcessParameters]
ScrewSpeed=90.0
ProcessType=throughput
xxDeltaP=200.0[kPa]
MassThroughput=240.00000000
MaterialTemperature=234.00000000
BarrelTemperature=250.00000000
ScrewTemperature=_INVALID_
BarrelTemperatureAdiabatic=NO
ScrewTemperatureAdiabatic=YES

[E3DProcessParameters/Material]
Name=Moplen HP501N
Type=Polymer
LimitViscoMin=1.00000000
LimitViscoMax=1000.00000000
[E3DProcessParameters/Material/RheologicalData]
CalcVisco=Carreau
CalcTemp=TbTs
[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=762.91800000
RecipVelocity=0.02663000
Exponent=0.64634000
[E3DProcessParameters/Material/RheologicalData/TbTs]
StandardTemperature=1.01987000
ReferenceTemperature=230.00000000
[E3DProcessParameters/Material/ThermoData]
HeatConductivitySlope=0.00008800
HeatConductivity=0.12080000
HeatCapacity=2.24900000
HeatCapacitySlope=0.00441800
DensityModel=Density
[E3DProcessParameters/Material/ThermoData/Density]
Density=0.87951300
DensitySlope=0.00056500

[E3DSimulationsettings]
HexMesher=TwinScrew
MeshQuality=coarse
AutomaticTimeStepControl = Yes
TimeStepEnlargmentFactor = 6.0
KTPRelease=NO

[E3DSimulationsettings/Output]
nOf1DLayers=16
nOfHistogramBins=24
HistogramShearMax=1e4
HistogramShearMin=1e-1
HistogramViscoMax=7000.0
CutDtata_1D=0.033

"""

INOUT1 = """

INPUT

Drehzahl (1/min):
400
Durchsatz (kg/h):
300
Gehäusetemperatur (°C):
Optional
270
Materialtemperatur (°C):
285
Zylinderdurchmesser:
Optional
51.5
Achsabstand:
Optional
41,5
Material:
PET1
Nicht-isotherm inkl. Particle Tracing

PET1
Wärmeleitfähigkeit: 0,22 W/mK
Wärmekapa: 1,93 kJ/kgK
Dichte: 1180 kg/m3

A 173,1447 Pa*s
B 0,002 s
C 0,04931
T:B 285°C
T:S 125°C

Zylinderdurchmesser:
51.5 mm
Achsabstand:
41,5 mm
Laenge:
41 mm
Kerndurchmesser:
30,9 mm
Schneckendurchmesser:
50,7 mm
Schneckenspiel,GapScrewScrew:
0,72 mm

screw_-Y_extended_by_10.off,screw_+Y_extended_by_10.off & type=OFF_LR

vcut :: 0.38mm
srid :: 11115

eingaengig, single flight : NoOfFlights=1

OUTPUT::

[SigmaFileInfo]
FileType=ToExtrud3D
FileVersion=SIGMA 10.0
Date=07/02/19
SigmaVersion=SIGMA 12.0.1(4492)
ConfigId=11115

[E3DGeometryData]
[E3DGeometryData/Machine]
Type=TSE
Unit=mm
Zwickel=straight
MachineName=XY 60
RotationDirection=LEFT
BarrelDiameter=51.5
CenterlineDistance=41.5
BarrelStraightCut=0.38
NoOfElements=1
NoOfFlights=1
BarrelLength=41.0

[E3DGeometryData/Machine/Element_1]
GapScrewScrew=0.72
ObjectType=screw
Unit=mm
startposition=0.0
off_filelistL=screw_-Y_extended_by_10.off
off_filelistR=screw_+Y_extended_by_10.off
innerdiameter=30.9
type=OFF_LR

[E3DProcessParameters]
ScrewSpeed=400.0
ProcessType=THROUGHPUT
MassThroughput=300.0
MaterialTemperature=285.0
BarrelTemperature=270.0
ScrewTemperature=_INVALID_
BarrelTemperatureAdiabatic=NO
ScrewTemperatureAdiabatic=YES

[E3DProcessParameters/Material]
Name=PET1
Type=Polymer

[E3DProcessParameters/Material/RheologicalData]
CalcVisco=Carreau
CalcTemp=TbTs

[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=173.15
RecipVelocity=0.002
Exponent=0.04931

[E3DProcessParameters/Material/RheologicalData/TBTS]
standardtemperature=125.0
referencetemperature=285.0

[E3DProcessParameters/Material/ThermoData]
heatconductivity=0.22
heatconductivityslope=0.0
heatcapacity=1.93
heatcapacityslope=0.0
densitymodel=DENSITY

[E3DProcessParameters/Material/ThermoData/Density]
Density=1.18
DensitySlope=0.0

[E3DSimulationsettings]
MeshQuality=medium
HexMesher=TwinScrew
KTPRelease=NO
"""

INOUT2 = """

INPUT

Geo	CHO_200_16D_KMB_V2
Laenge: 2780 mm
Zylinderdurchmesser: 200 mm
Maximaler Schneckendurchmesser: 199,5 mm
Schneckenspiel: 0,25 mm
Minimaler Schneckendurchmesser: 108 mm
Durchmesser am Anfang: 108 mm


process parameters:
Durchsatz	816	Kg/h
T_screw	92	°C
T_barrel	86	°C
RPM	10

Material	SteadyShear_T1_nichtIsotherm_SA
A	311.743,16	Pa.s
B	2,681	s
C	0,90496
Tb	100	°C
Ts	-143,40	°C
cp	2	kJ/kg.K
lamda	0,2	W/mK
dichte	1147	kg/m³

OUTPUT

[SigmaFileInfo]
FileType=ToExtrud3D
FileVersion=SIGMA 10.0
Date=07/02/19
SigmaVersion=SIGMA 12.0.1(4492)
ConfigId=CHO_200_16D_KMB_V2.xpro-YYYYMMDDhhmm

[E3DGeometryData]
[E3DGeometryData/Machine]
Type=SSE
Unit=mm
Zwickel=straight
MachineName=CHO_200_16D_KMB_V2
RotationDirection=LEFT
BarrelDiameter=200.0
CenterlineDistance=_INVALID_
BarrelStraightCut=_INVALID_
NoOfElements=1
NoOfFlights=1
BarrelLength=2780.0

[E3DGeometryData/Machine/Element_1]
GapScrewScrew=0.25
ObjectType=screw
Unit=mm
startposition=0.0
innerdiameter=108.0
outerdiameter=199.5
type=OFF
off_filelist=screw_extended_by_10.off

[E3DProcessParameters]
ScrewSpeed=10.0
ProcessType=THROUGHPUT
MassThroughput=816.0
MaterialTemperature=92.0
BarrelTemperature=86.0
ScrewTemperature=92.0
BarrelTemperatureAdiabatic=NO
ScrewTemperatureAdiabatic=NO

[E3DProcessParameters/Material]
Name=SteadyShear_T1_nichtIsotherm_SA
Type=Polymer

[E3DProcessParameters/Material/RheologicalData]
CalcVisco=Carreau
CalcTemp=TbTs

[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=311743.16
RecipVelocity=2.681
Exponent=0.90496

[E3DProcessParameters/Material/RheologicalData/TBTS]
standardtemperature=-143.40
referencetemperature=100.0

[E3DProcessParameters/Material/ThermoData]
heatconductivity=0.2
heatconductivityslope=0.0
heatcapacity=2.0
heatcapacityslope=0.0
densitymodel=DENSITY

[E3DProcessParameters/Material/ThermoData/Density]
Density=1.147
DensitySlope=0.0

[E3DSimulationsettings]
MeshQuality=medium
HexMesher=HollowCylinder
KTPRelease=NO


"""


BEHAVIOR_STRING_OM= f"""
You are an assistant for creating INI file. You can take this INI file as a template:
[SigmaFileInfo] FileType=ToExtrud3D FileVersion=SIGMA 10.0 Date={date_string_short} SigmaVersion=SIGMA 12.0.1(4492) ConfigId=XY60_PE_400.xpro-201907020948 [E3DGeometryData] [E3DGeometryData/Machine] Type=TSE Unit=mm Zwickel=straight MachineName=XY 60 RotationDirection=LEFT BarrelDiameter=51.5 CenterlineDistance=41.5 BarrelStraightCut=0.4 NoOfElements=1 NoOfFlights=1 BarrelLength=41.0 [E3DGeometryData/Machine/Element_1] GapScrewScrew=0.7 ObjectType=screw Unit=mm startposition=0.0 off_filelistL=screw_-Y_extended_by_10.off off_filelistR=screw_+Y_extended_by_10.off innerdiameter=30.9 type=OFF_LR [E3DProcessParameters] ScrewSpeed=400.0 ProcessType=THROUGHPUT MassThroughput=300.0 MaterialTemperature=285.0 BarrelTemperature=270.0 ScrewTemperature=_INVALID_ BarrelTemperatureAdiabatic=NO ScrewTemperatureAdiabatic=YES [E3DProcessParameters/Material] Name=PET1 Type=Polymer [E3DProcessParameters/Material/RheologicalData] CalcVisco=Carreau CalcTemp=TbTs [E3DProcessParameters/Material/RheologicalData/Carreau] ZeroViscosity=173.15 RecipVelocity=0.002 Exponent=0.04931 [E3DProcessParameters/Material/RheologicalData/TBTS] standardtemperature=125.0 referencetemperature=285.0 [E3DProcessParameters/Material/ThermoData] heatconductivity=0.22 heatconductivityslope=0.0 heatcapacity=1.93 heatcapacityslope=0.0 densitymodel=DENSITY [E3DProcessParameters/Material/ThermoData/Density] Density=1.18 DensitySlope=0.0 [E3DSimulationsettings] MeshQuality=medium HexMesher=TwinScrew KTPRelease=NO
A user may now send a message in which he defines one or more key value pairs. Your task is to find and replace the values in the template by the value(s) given in user's message. Your reply always includes the full, updated INI file. A user may enter keys in the German language if so try to find the matching key and replace its value.
in case that some of the inputs are not available, report those missing parameters or expected inconsistencies below the generated INI file. inhere are some basic descriptions to the individual parameters and some initial/default values : {EXPLANATION_STRING_OM}.
I have put the information in angled brackets after the key-value pairs. in the square brackets are the units in which the parameters should be provided in the INI file, therefore you might need to convert the user provided inputs into the expected units.

here some examples for typical inputs and outputs:
{INOUT1}

{INOUT2}

and for an implicitly defined screw sequence the outputfile only:
{OUT3}

important additional output for statistics::
write out the number of input and out tokens

"""
