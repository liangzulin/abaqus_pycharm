
import os
import sys

ON = 1
OFF = 0


class MeshOptions:
    def setValues(self, meshTechnique=ON):
        pass


class AssemblyDisplay:
    def __init__(self):
        self.meshOptions = MeshOptions()

    def setValues(self, optimizationTasks=None, geometricRestrictions=None, stopConditions=None,
                  adaptiveMeshConstraints=None, step=None, loads=ON, bcs=ON, predefinedFields=ON, connectors=ON,
                  mesh=ON):
        pass


class ViewportsClass:
    def __init__(self):
        self.view = View()
        self.assemblyDisplay = AssemblyDisplay()

    def makeCurrent(self):
        pass

    def maximize(self):
        pass

    def setValues(self, displayedObject):
        pass

    class PartDisplay:
        def __init__(self):
            self.meshOptions = MeshOptions()

        def setValues(self, sectionAssignments, engineeringFeatures, mesh=ON):
            pass

        class GeometryOptions:
            def setValues(self, referenceRepresentation):
                pass

        geometryOptions = GeometryOptions()

    partDisplay = PartDisplay()
    # partDisplay.geometryOptions.setValues(referenceRepresentation=ON)


class View:
    def setValues(self, nearPlane=105.916, farPlane=184.101, width=120.322, height=54.5645, viewOffsetX=12.107,
                  viewOffsetY=-0.105324, cameraPosition=None, cameraUpVector=None, cameraTarget=None):
        pass


class Session:

    def __init__(self):
        """
        This object is not from the abaqus file, just temporaly code here, will be move in future
        """
        self.viewports = {}

    # viewports = {'Viewport: 1': ViewportsClass()}

    # @staticmethod
    def Viewport(self, name, origin=None, width=None, height=None):

        self.viewports[name] = ViewportsClass()


session = Session()  # default abaqus instance


class Edges:
    def getSequenceFromMask(self, mask):
        pass


class AssemblyInstance:
    def __init__(self):
        self.edges = Edges()


class Assembly:

    def __init__(self):
        """
        This method is not from the abaqus file, just temporaly code here, will be move in future
        """
        self.instances = {}

    def regenerate(self):
        pass

    def DatumCsysByDefault(self, CARTESIAN):
        pass

    def Instance(self, name, part, dependent):
        self.instances[name] = AssemblyInstance()

    def Set(self, edges, name):
        pass

    def Surface(self, side1Edges, name):
        pass


class ConstrainedSketch:

    def __init__(self):
        self.constraints = None
        self.dimensions = None
        self.vertices = None
        self.geometry = [i for i in range(10000 ** 2)]

    def setPrimaryObject(self, option):
        pass

    def Line(self, point1, point2):
        pass

    def HorizontalConstraint(self, entity, addUndoState):
        pass

    def unsetPrimaryObject(self):
        pass


class Faces:
    def getSequenceFromMask(self, mask):
        pass


class Region:
    def __init__(self):
        pass


class Parts:
    def __init__(self):
        self.faces = Faces()

    def BaseShellExtrude(self, sketch, depth):
        pass

    def Set(self, faces, name):
        return Region()

    def SectionAssignment(self, region, sectionName, offset, offsetType, offsetField, thicknessAssignment):
        pass

    def seedPart(self, size, deviationFactor, minSizeFactor):
        pass

    def generateMesh(self):
        pass

    def setElementType(self, regions, elemTypes):
        pass

    def addNodes(self, nodeData, nodeSetName='nset-1'):
        pass

    def addElements(self, elementData, type, elementSetName=None, sectionCategory=None):
        # type: (object, str, str, SectionCategoryClass) -> None
        pass


class MaterialClass:
    def Elastic(self, table=None, type=None, temperatureDependency=OFF, dependencies=0, noCompression=OFF, noTension=OFF,
                moduli=None):
        pass


class Load:
    def setValues(self, magnitude):
        pass


class Model:
    def __init__(self):
        """
        This method is not from the abaqus file
        """
        self.parts = {}
        self.sketches = {}
        self.materials = {}
        self.loads = {}
        self.rootAssembly = Assembly()

    def Part(self, name, dimensionality, type):
        self.parts[name] = Parts()

    def ConstrainedSketch(self, name, sheetSize):
        self.sketches[name] = None
        return ConstrainedSketch()

    def Material(self, name):
        self.materials[name] = MaterialClass()

    def HomogeneousShellSection(self, name, preIntegrate, material, thicknessType,
                                thickness, thicknessField, idealization,
                                poissonDefinition, thicknessModulus, temperature,
                                useDensity, integrationRule, numIntPts):
        pass

    def StaticStep(self, name='Step-1', previous='Initial', maxNumInc=1000, initialInc=0.001, nlgeom=None):
        # type: (str, str, int, float, object) -> None
        pass

    def DisplacementBC(self, name='BC-1', createStepName='Step-1',
                       region=None, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0,
                       amplitude=None, fixed=None, distributionType=None, fieldName='',
                       localCsys=None):
        pass

    def ShellEdgeLoad(self, name='Load-1', createStepName='Step-1',
                      region=None, magnitude=5.0, distributionType=None, field='',
                      localCsys=None):
        self.loads[name] = Load()


class Mdb:
    """
    default abaqus object
    """

    def __init__(self):
        self.models = {'Model-1': Model()}
        # Addition method here
        # self.abaqus_bat_path = 'D:\\SIMULIA\\Abaqus\\Commands\\abaqus'
        self.abaqus_bat_path = 'abaqus'
        self.abaqus_bat_setting = 'noGUI'
        self.debug = True

    def Job(self, name='zigzag', model='Model-1', description='', type=None,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=None, getMemoryFromAnalysis=True,
            explicitPrecision=None, nodalOutputPrecision=None, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=None, multiprocessingMode=None, numCpus=1,
            numGPUs=0):
        pass

    # nonlocal abaqus_bat_setting
    # abaqus_bat_setting_in = abaqus_bat_setting

    def saveAs(self, pathName):
        if isinstance(self.debug, bool) and self.debug:
            print(pathName)
        if 'ABAQUS_BAT_SETTING' in os.environ.keys():
            self.abaqus_bat_setting = os.environ['ABAQUS_BAT_SETTING']
        if 'ABAQUS_BAT_PATH' in os.environ.keys():
            self.abaqus_bat_path = os.environ['ABAQUS_BAT_PATH']
        os.system(self.abaqus_bat_path + ' cae -' + self.abaqus_bat_setting + ' ' + os.path.abspath(sys.argv[0]))


mdb = Mdb()  # default abaqus instance
