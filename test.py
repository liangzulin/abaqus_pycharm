from os import environ
from abaqus import *
from abaqusConstants import *
from caeModules import mesh
from driverUtils import executeOnCaeStartup

environ['ABAQUS_BAT_PATH'] = 'D:\\SIMULIA\\Abaqus\\Commands\\abaqus'
environ['ABAQUS_BAT_SETTING'] = 'noGUI'

session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=300, height=140)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()

executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=ON)
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)  # type: ConstrainedSketch
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
"""
s <type 'ConstrainedSketch'>
g <type 'Repository'>
v <type 'Repository'>
d <type 'Repository'>
c <type 'Repository'>
"""

s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(-20.0, 10.0), point2=(-15.0, 0.0))
s.Line(point1=(-15.0, 0.0), point2=(-20.0, -10.0))
s.Line(point1=(-20.0, -10.0), point2=(20.0, -10.0))
s.HorizontalConstraint(entity=g[4], addUndoState=False)
s.Line(point1=(20.0, -10.0), point2=(15.0, 0.0))
s.Line(point1=(15.0, 0.0), point2=(20.0, 10.0))
s.Line(point1=(20.0, 10.0), point2=(-20.0, 10.0))
s.HorizontalConstraint(entity=g[7], addUndoState=False)
s.Line(point1=(-30.0, 0.0), point2=(-15.0, 0.0))
s.HorizontalConstraint(entity=g[8], addUndoState=False)
s.Line(point1=(15.0, 0.0), point2=(30.0, 0.0))
s.HorizontalConstraint(entity=g[9], addUndoState=False)
# p = ;
mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']  # type: Parts
p.BaseShellExtrude(sketch=s, depth=20.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=105.916,
                                                farPlane=184.101, width=120.322, height=54.5645, viewOffsetX=12.107,
                                                viewOffsetY=-0.105324)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
                                                       engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((210000.0, 0.3), ))
mdb.models['Model-1'].HomogeneousShellSection(name='Section-1',
                                              preIntegrate=OFF, material='Material-1', thicknessType=UNIFORM,
                                              thickness=0.15, thicknessField='', idealization=NO_IDEALIZATION,
                                              poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
                                              useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#ff ]',), )
region = p.Set(faces=faces, name='Set-1')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(optimizationTasks=OFF, geometricRestrictions=OFF,
                                                           stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly  # type: Assembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON)
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial',
                                 maxNumInc=1000, initialInc=0.001, nlgeom=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON,
                                                           predefinedFields=ON, connectors=ON,
                                                           adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Part-1-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#400000 ]',), )
region = a.Set(edges=edges1, name='Set-1')
mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1',
                                     region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0,
                                     amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',
                                     localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=120.889,
                                                farPlane=166.432, width=94.7412, height=42.9641,
                                                cameraPosition=(7.96252,
                                                                70.7189, 134.832),
                                                cameraUpVector=(-0.313976, 0.610657, -0.726992),
                                                cameraTarget=(2.5404, -2.07841, 9.53802))
session.viewports['Viewport: 1'].view.setValues(nearPlane=109.312,
                                                farPlane=180.107, width=85.6687, height=38.8498,
                                                cameraPosition=(73.2145,
                                                                72.2883, 111.799),
                                                cameraUpVector=(-0.416043, 0.637935, -0.648033),
                                                cameraTarget=(1.92831, -2.09313, 9.75408))
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].edges
side1Edges1 = s1.getSequenceFromMask(mask=('[#100000 ]',), )
region = a.Surface(side1Edges=side1Edges1, name='Surf-1')
mdb.models['Model-1'].ShellEdgeLoad(name='Load-1', createStepName='Step-1',
                                    region=region, magnitude=5.0, distributionType=UNIFORM, field='',
                                    localCsys=None)
mdb.models['Model-1'].loads['Load-1'].setValues(magnitude=-5.0)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF,
                                                           bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF,
                                                       engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(meshTechnique=ON)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD,
                          secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=S3, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
faces = f.getSequenceFromMask(mask=('[#ff ]',), )
pickedRegions = (faces,)
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.Job(name='zigzag', model='Model-1', description='', type=ANALYSIS,
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
        numGPUs=0)
mdb.saveAs(pathName='zigzag')
#: The model database has been saved to "zigzag.cae".
