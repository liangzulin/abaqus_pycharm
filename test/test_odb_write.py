"""odbWrite.py
   Script to create an output database and add model,
   field, and history data. The script also reads
   history data, performs an operation on the data, and writes
   the result back to the output database.
   usage: abaqus python odbWrite.py
"""

from os import environ
try:
    from import_file.odbAccess import *
    from import_file.odbMaterial import *
    from import_file.odbSection import *
    from import_file.abaqusConstants import *
except ImportError as e:
    print(e, '\n\n\n\n\n\n')
    from odbAccess import *
    from odbMaterial import *
    from odbSection import *
    from abaqusConstants import *

environ['ABAQUS_BAT_PATH'] = 'D:\\SIMULIA\\Abaqus\\Commands\\abaqus'
environ['ABAQUS_BAT_SETTING'] = 'script'


def createODB():
    # Create an ODB (which also creates the rootAssembly)
    odb = Odb(name='simpleModel',
              analysisTitle='ODB created with Python ODB API',
              description='example illustrating Python ODB API ',
              path='odbWritePython.odb')

    # create few materials
    materialName = "Elastic Material"
    material_1 = odb.Material(name=materialName)
    material_1.Elastic(type=ISOTROPIC,
                       temperatureDependency=OFF, dependencies=0,
                       noCompression=OFF, noTension=OFF,
                       moduli=LONG_TERM, table=((12000, 0.3),))

    # create few sections
    sectionName = 'Homogeneous Shell Section'
    section_1 = odb.HomogeneousShellSection(name=sectionName,
                                            material=materialName, thickness=2.0)
    #  Model data:

    # Set up the section categories.
    sCat = odb.SectionCategory(name='S5',
                               description='Five-Layered Shell')
    spBot = sCat.SectionPoint(number=1,
                              description='Bottom')
    spMid = sCat.SectionPoint(number=3,
                              description='Middle')
    spTop = sCat.SectionPoint(number=5,
                              description='Top')

    #  Create a 2-element shell model,
    #  4 integration points, 5 section points.

    part1 = odb.Part(name='part-1', embeddedSpace=THREE_D,
                     type=DEFORMABLE_BODY)
    nodeData = (
        (1, 1, 0, 0),
        (2, 2, 0, 0),
        (3, 2, 1, 0.1),
        (4, 1, 1, 0.1),
        (5, 2, -1, -0.1),
        (6, 1, -1, -0.1),
    )
    part1.addNodes(nodeData=nodeData,
                   nodeSetName='nset-1')

    elementData = (
        (1, 1, 2, 3, 4),
        (2, 6, 5, 2, 1),
    )
    part1.addElements(elementData=elementData, type='S4',
                      elementSetName='eset-1', sectionCategory=sCat)

    #  Instance the part.
    instance1 = odb.rootAssembly.Instance(name='part-1-1',
                                          object=part1)
    # create instance level sets for section assignment
    elLabels = (1, 2)
    elset_1 = odb.rootAssembly.instances['part-1-1']. \
        ElementSetFromElementLabels(name=materialName,
                                    elementLabels=elLabels)
    instance1.assignSection(region=elset_1,
                            section=section_1)

    #  Field data:

    #  Create a step and a frame.

    step1 = odb.Step(name='step-1',
                     description='first analysis step',
                     domain=TIME, timePeriod=1.0)
    analysisTime = 0.1
    frame1 = step1.Frame(incrementNumber=1,
                         frameValue=analysisTime,
                         description='results frame for time ' + str(analysisTime))

    #  Write nodal displacements.

    uField = frame1.FieldOutput(name='U', description='Displacements', type=VECTOR)

    nodeLabelData = (1, 2, 3, 4, 5, 6)
    dispData = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (10, 11, 12),
        (13, 14, 15),
        (16, 17, 18)
    )

    uField.addData(position=NODAL, instance=instance1,
                   labels=nodeLabelData,
                   data=dispData)

    #  Make this the default deformed field for visualization.

    step1.setDefaultDeformedField(uField)

    """ Write stress tensors
    (output only available at top/bottom section points)
    The element defined above (S4) has 4 integration points.
    Hence, there are 4 stress tensors per element.
    Each Field constructor refers to only one layer of section
    points.
    """

    elementLabelData = (1, 2)
    topData = (
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
    )
    bottomData = (
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
        (1., 2., 3., 4.),
    )

    transform = (
        (1., 0., 0.),
        (0., 1., 0.),
        (0., 0., 1.)
    )

    sField = frame1.FieldOutput(name='S', description='Stress', type=TENSOR_3D_PLANAR)
    sField.addData(position=INTEGRATION_POINT,
                   sectionPoint=spTop, instance=instance1,
                   labels=elementLabelData, data=topData,
                   localCoordSystem=transform)
    sField.addData(position=INTEGRATION_POINT,
                   sectionPoint=spBot, instance=instance1,
                   labels=elementLabelData, data=bottomData,
                   localCoordSystem=transform)

    #  For this step, make this the default field
    #  for visualization.

    step1.setDefaultField(sField)

    #  History data:

    #  Create a HistoryRegion for a specific point.

    hRegionStep1 = step1.HistoryRegion(name='historyNode0',
                                       description='Displacement and reaction force',
                                       point=instance1.nodes[0])

    #  Create variables for this history output in step1.

    hOutputStep1U1 = hRegionStep1.HistoryOutput(name='U1',
                                                description='Displacement', type=SCALAR)
    hOutputStep1Rf1 = hRegionStep1.HistoryOutput(name='RF1',
                                                 description='Reaction Force', type=SCALAR)

    #  Add history data for step1.

    timeData1 = (0.0, 0.1, 0.3, 1.0)
    u1Data = (0.0, 0.1, 0.3, 0.5)
    rf1Data = (0.0, 0.1, 0.3, 0.5)

    hOutputStep1U1.addData(frameValue=timeData1,
                           value=u1Data)
    hOutputStep1Rf1.addData(frameValue=timeData1,
                            value=rf1Data)

    #  Create another step for history data.
    step2 = odb.Step(name='step-2', description='',
                     domain=TIME, timePeriod=1.0)
    hRegionStep2 = step2.HistoryRegion(
        name='historyNode0',
        description='Displacement and reaction force',
        point=instance1.nodes[0])
    hOutputStep2U1 = hRegionStep2.HistoryOutput(
        name='U1',
        description='Displacement',
        type=SCALAR)
    hOutputStep2Rf1 = hRegionStep2.HistoryOutput(
        name='RF1',
        description='Reaction Force',
        type=SCALAR)

    #  Add history data for the second step.
    timeData2 = (1.2, 1.9, 3.0, 4.0)
    u1Data = (0.8, 0.9, 1.3, 1.5)
    rf1Data = (0.9, 1.1, 1.3, 1.5)

    hOutputStep2U1.addData(frameValue=timeData2,
                           value=u1Data)
    hOutputStep2Rf1.addData(frameValue=timeData2,
                            value=rf1Data)

    # Get XY Data from the two steps.
    u1FromStep1 = hRegionStep1.getSubset(variableName='U1')
    u1FromStep2 = hRegionStep2.getSubset(variableName='U1')

    # Square the history data.
    u1SquaredFromStep1 = \
        power(u1FromStep1.historyOutputs['U1'], 2.0)
    u1SquaredFromStep2 = \
        power(u1FromStep2.historyOutputs['U1'], 2.0)

    # Add the squared displacement to the two steps.
    hOutputStep1sumU1 = hRegionStep1.HistoryOutput(
        name='squareU1',
        description='Square of displacements',
        type=SCALAR)
    hOutputStep1sumU1.addData(data=u1SquaredFromStep1.data)

    hOutputStep2sumU1 = hRegionStep2.HistoryOutput(
        name='squareU1',
        description='Square of displacements',
        type=SCALAR)
    hOutputStep2sumU1.addData(data=u1SquaredFromStep2.data)

    # Save the results in the output database.
    # Use the Visualization module of Abaqus/CAE to
    # view the contents of the output database.

    odb.save()
    odb.close()


if __name__ == "__main__":
    createODB()
