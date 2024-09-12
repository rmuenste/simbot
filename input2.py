
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
