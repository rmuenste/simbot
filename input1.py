
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
