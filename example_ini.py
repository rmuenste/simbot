EXAMPLE_INI = """
[SigmaFileInfo]
FileType=undefined ; Internal parameter identifying the file type
FileVersion=undefined ; Internal version parameter
Date=undefined ; The current date
SigmaVersion=undefined ; Internal version of SIGMA used
ConfigId=undefined ; Internal system job ID, user may refer to this as srid

[E3DGeometryData]
[E3DGeometryData/Machine]
Type=undefined ; Extruder type, possible values: TSE, SSE, DIE
Unit=undefined ; Unit for input parameters, mm, cm, dm, m, ... etc.
Zwickel=undefined ; Barrel shape; can be straight or curved
MachineName=undefined ; Extruder name
RotationDirection=undefined ; Extruder rotation direction: LEFT (default) or RIGHT
BarrelDiameter=undefined ; Barrel diameter (default: 2 * screw diameter + 2 * screw clearance), German: Zylinderdurchmesser [mm]
CenterlineDistance=undefined ; Centerline distance between axes, required for TSE simulations [mm]
BarrelStraightCut=undefined ; Depth of the V-cut (default: 2.5 percent of BarrelDiameter, used only for twin screws), user may refer to this as vcut [mm]
NoOfElements=undefined ; Number of elements in the extruder
NoOfFlights=undefined ; Number of flights in the extruder, can use single flight (German: eingängig)
BarrelLength=undefined ; Length of the barrel/housing, German: Länge, Gehäuselänge or similar [mm]

[E3DGeometryData/Machine/Element_1]
GapScrewScrew=undefined ; Clearance between screws in a twin-screw extruder, German: Schneckenspiel [mm]
ObjectType=undefined ; The object is a screw
Unit=undefined ; Unit for input parameters, mm, cm, dm, m, ... etc.
startposition=undefined ; Starting position of the screw [mm]
off_filelist=undefined ; File containing the 3D geometry of the screw, this key-value is used if type=OFF in this section
off_filelistL=undefined ; File for the left-hand side of the screw geometry, this key-value is used if type=OFF_LR in this section
off_filelistR=undefined ; File for the right-hand side of the screw geometry, this key-value is used if type=OFF_LR in this section
innerdiameter=undefined ; Inner diameter of the screw, German: Kerndurchmesser, Maximaler Schneckendurchmesser [mm]
outerdiameter=undefined ; Outer diameter of the screw, German: Minimaler Schneckendurchmesser [mm]
type=undefined ; Type of input geometry; OFF requires `off_filelist`, OFF_LR requires both `off_filelistL` and `off_filelistR`

[E3DProcessParameters]
ScrewSpeed=undefined ; Rotational speed of the screw [rpm]
ProcessType=undefined ; Type of process: mass throughput, can be: THROUGHPUT
MassThroughput=undefined ; Mass of material processed per hour, German: Durchsatz, Massendurchsatz [kg/h]
MaterialTemperature=undefined ; Inflow temperature of the material and starting melt temperature [C deg]
BarrelTemperature=undefined ; Barrel temperature (used if not adiabatic); can be called T_barrel [C deg]
ScrewTemperature=undefined ; Screw temperature (used if not adiabatic); can be called T_screw [C deg]
BarrelTemperatureAdiabatic=undefined ; If NO, a specific ScrewTemperature must be defined, can be YES, NO
ScrewTemperatureAdiabatic=undefined ; If NO, a specific BarrelTemperature must be defined, can be YES, NO

[E3DProcessParameters/Material]
Name=undefined ; Name of the material
Type=undefined ; Type of material

[E3DProcessParameters/Material/RheologicalData]
CalcVisco=undefined ; Viscosity model used for the material, can be: Carreau
CalcTemp=undefined ; Temperature model used for the material, can be: TbTs

[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=undefined ; Viscosity at zero shear rate, a user may refer to as A which comes from the Carreau model formula [Pa.s]
RecipVelocity=undefined ; Reciprocal of the characteristic shear rate velocity, can be called B [s]
Exponent=undefined ; Exponent in the Carreau viscosity model, can be called C [unitless]

[E3DProcessParameters/Material/RheologicalData/TBTS]
standardtemperature=undefined ; Standard processing temperature, user may refer to this as T:S or similar [C deg]
referencetemperature=undefined ; Reference temperature for rheological calculations, user may refer to this as T:B or similar [C deg]

[E3DProcessParameters/Material/ThermoData]
heatconductivity=undefined ; Thermal conductivity of the material [W/m/K]
heatconductivityslope=undefined ; Slope of the thermal conductivity with respect to temperature
heatcapacity=undefined ; Specific heat capacity of the material, can be cp [kJ/kg/K]
heatcapacityslope=undefined ; Slope of the heat capacity with respect to temperature
densitymodel=undefined ; Density model used for the material, can be: DENSITY

[E3DProcessParameters/Material/ThermoData/Density]
Density=undefined ; Density of the melt [g/cm3]
DensitySlope=undefined ; Slope of the density with respect to temperature

[E3DSimulationsettings]
MeshQuality=undefined ; Mesh resolution, can be: coarse, medium, fine
HexMesher=undefined ; Mesh generator type: TwinScrew or HollowCylinder
KTPRelease=undefined ; Flag indicating whether KTP release is activated; NO or YES
"""