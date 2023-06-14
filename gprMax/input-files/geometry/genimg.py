# trace generated using paraview version 5.11.0
import json
import mmap
import os
import shutil
from xml.etree import ElementTree as ET
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

folder_path = os.getcwd()

folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

filtered_folders = [f for f in folders if f.startswith('RebarCorrosion_') and not any(fail.endswith('.png') for fail in os.listdir(os.path.join(folder_path, f)))]

for folder in filtered_folders:
    # create a new 'XML Image Data Reader'
    gprDatavti = XMLImageDataReader(registrationName='gprData.vti', FileName=[f'{folder_path}\{folder}\gprData.vti'])
    gprDatavti.CellArrayStatus = ['Material', 'Sources_PML', 'Receivers']

    # Properties modified on gprDatavti
    gprDatavti.TimeArray = 'None'

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    gprDatavtiDisplay = Show(gprDatavti, renderView1, 'UniformGridRepresentation')

    # trace defaults for the display properties.
    gprDatavtiDisplay.Representation = 'Outline'
    gprDatavtiDisplay.ColorArrayName = ['CELLS', '']
    gprDatavtiDisplay.SelectTCoordArray = 'None'
    gprDatavtiDisplay.SelectNormalArray = 'None'
    gprDatavtiDisplay.SelectTangentArray = 'None'
    gprDatavtiDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    gprDatavtiDisplay.SelectOrientationVectors = 'None'
    gprDatavtiDisplay.ScaleFactor = 0.03
    gprDatavtiDisplay.SelectScaleArray = 'Material'
    gprDatavtiDisplay.GlyphType = 'Arrow'
    gprDatavtiDisplay.GlyphTableIndexArray = 'Material'
    gprDatavtiDisplay.GaussianRadius = 0.0015
    gprDatavtiDisplay.SetScaleArray = [None, '']
    gprDatavtiDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    gprDatavtiDisplay.OpacityArray = [None, '']
    gprDatavtiDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    gprDatavtiDisplay.DataAxesGrid = 'GridAxesRepresentation'
    gprDatavtiDisplay.PolarAxes = 'PolarAxesRepresentation'
    gprDatavtiDisplay.ScalarOpacityUnitDistance = 0.009209928593820126
    gprDatavtiDisplay.OpacityArrayName = ['CELLS', 'Material']
    gprDatavtiDisplay.ColorArray2Name = ['CELLS', 'Material']
    gprDatavtiDisplay.IsosurfaceValues = [2.0]
    gprDatavtiDisplay.SliceFunction = 'Plane'
    gprDatavtiDisplay.SelectInputVectors = [None, '']
    gprDatavtiDisplay.WriteLog = ''

    # init the 'Plane' selected for 'SliceFunction'
    gprDatavtiDisplay.SliceFunction.Origin = [0.15, 0.1, 0.0005]

    # reset view to fit data
    renderView1.ResetCamera(False)

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # Read Paraview version number to set threshold filter method
    pvv = GetParaViewVersion()
    if pvv.major == 5 and pvv.minor < 10:
        new_thres = False
    else:
        new_thres = True

    def threshold_filt(input, lt, ut, scalars):
        """Create threshold filter according to Paraview version.
        
        Args:
            input (array): input data to threshold filter
            lt, ut (int): lower and upper bounds of thresholding operation
            scalars (list/str): name of scalar array to perform thresholding

        Returns:
            threshold (object): threshold filter
        """

        threshold = Threshold(Input=input)
        threshold.Scalars = scalars

        if new_thres:
            threshold.LowerThreshold = lt
            threshold.UpperThreshold = ut
        else:
            threshold.ThresholdRange = [lt, ut]

        return threshold


    def display_src_rx(srcs_rxs, dl):
        """Display sources and receivers as Paraview box sources.
            Only suitable for gprMax >= v4

        Args:
            srcs_rxs (list): source/receiver names and positions
            dl (tuple): spatial discretisation
        """

        for item in srcs_rxs:
            pos = item['position']
            name = item['name']
            src_rx = Box(Center=[pos[0] + dl[0]/2,
                                pos[1] + dl[1]/2,
                                pos[2] + dl[2]/2],
                        XLength=dl[0], YLength=dl[1], ZLength=dl[2])
            RenameSource(name, src_rx)
            Show(src_rx)


    def display_pmls(pmlthick, dx_dy_dz, nx_ny_nz):
        """Display PMLs as box sources using PML thickness values.
            Only suitable for gprMax >= v4

        Args:
            pmlthick (tuple): PML thickness values for each slab (cells)
            dx_dy_dz (tuple): Spatial resolution (m)
            nx_ny_dz (tuple): Domain size (cells)
        """

        pml_names = ['x0', 'y0', 'z0', 'xmax', 'ymax', 'zmax']
        pmls = dict.fromkeys(pml_names, None)

        if pmlthick[0] != 0:
            x0 = Box(Center=[pmlthick[0] * dx_dy_dz[0] / 2,
                            nx_ny_nz[1] * dx_dy_dz[1] / 2,
                            nx_ny_nz[2] * dx_dy_dz[2] / 2],
                    XLength=pmlthick[0] * dx_dy_dz[0],
                    YLength=nx_ny_nz[1] * dx_dy_dz[1],
                    ZLength=nx_ny_nz[2] * dx_dy_dz[2])
            pmls['x0'] = x0

        if pmlthick[3] != 0:
            xmax = Box(Center=[dx_dy_dz[0] * (nx_ny_nz[0] - pmlthick[3] / 2),
                            nx_ny_nz[1] * dx_dy_dz[1] / 2,
                            nx_ny_nz[2] * dx_dy_dz[2] / 2],
                    XLength=pmlthick[3] * dx_dy_dz[0],
                    YLength=nx_ny_nz[1] * dx_dy_dz[1],
                    ZLength=nx_ny_nz[2] * dx_dy_dz[2])
            pmls['xmax'] = xmax

        if pmlthick[1] != 0:
            y0 = Box(Center=[nx_ny_nz[0] * dx_dy_dz[0] / 2,
                            pmlthick[1] * dx_dy_dz[1] / 2,
                            nx_ny_nz[2] * dx_dy_dz[2] / 2],
                    XLength=nx_ny_nz[0] * dx_dy_dz[0],
                    YLength=pmlthick[1] * dx_dy_dz[1],
                    ZLength=nx_ny_nz[2] * dx_dy_dz[2])
            pmls['y0'] = y0

        if pmlthick[4] != 0:
            ymax = Box(Center=[nx_ny_nz[0] * dx_dy_dz[0] / 2,
                            dx_dy_dz[1] * (nx_ny_nz[1] - pmlthick[4] / 2),
                            nx_ny_nz[2] * dx_dy_dz[2] / 2],
                    XLength=nx_ny_nz[0] * dx_dy_dz[0],
                    YLength=pmlthick[4] * dx_dy_dz[1],
                    ZLength=nx_ny_nz[2] * dx_dy_dz[2])
            pmls['ymax'] = ymax

        if pmlthick[2] != 0:
            z0 = Box(Center=[nx_ny_nz[0] * dx_dy_dz[0] / 2,
                            nx_ny_nz[1] * dx_dy_dz[1] / 2,
                            pmlthick[2] * dx_dy_dz[2] / 2],
                    XLength=nx_ny_nz[0] * dx_dy_dz[0],
                    YLength=nx_ny_nz[1] * dx_dy_dz[1],
                    ZLength=pmlthick[2] * dx_dy_dz[2])
            pmls['z0'] = z0

        if pmlthick[5] != 0:
            zmax = Box(Center=[nx_ny_nz[0] * dx_dy_dz[0] / 2,
                            nx_ny_nz[1] * dx_dy_dz[1] / 2,
                            dx_dy_dz[2] * (nx_ny_nz[2] - pmlthick[5] / 2)],
                    XLength=nx_ny_nz[0] * dx_dy_dz[0],
                    YLength=nx_ny_nz[1] * dx_dy_dz[1],
                    ZLength=pmlthick[5] * dx_dy_dz[2])
            pmls['zmax'] = zmax

        # Name PML sources and set opacity
        tmp = []
        for pml in pmls:
            if pmls[pml]:
                RenameSource('PML - ' + pml, pmls[pml])
                Hide(pmls[pml], renderview)
                tmp.append(pmls[pml])

        # Create a group of PMLs to switch on/off easily
        if tmp:
            pml_gp = AppendDatasets(Input=tmp)
            RenameSource('PML - All', pml_gp)
            pml_view = Show(pml_gp)
            pml_view.Opacity = 0.5


    # Get whatever source is loaded (should be model)
    model = GetActiveSource()

    # Get active view
    renderview = GetActiveView()

    # Show Data Axes Grid
    renderview.AxesGrid.Visibility = 1

    # Hide display of root data
    Hide(model)


    #####################################
    # Get filename or list of filenames #
    #####################################

    # Single .vti or .vtu file
    if len(model.FileName) == 1:
        files = model.FileName
        dirname = os.path.dirname(files[0])

    # Multiple .vti or .vtu files referenced in a .pvd file 
    else:
        files = []
        dirname = os.path.dirname(model.FileName)
        tree = ET.parse(model.FileName)
        root = tree.getroot()
        for elem in root:
            for subelem in elem.findall('DataSet'):
                tmp = os.path.join(dirname, subelem.get('file'))
                files.append(tmp)

    # Dictionaries to hold data - mainly for <v4 behaviour
    materials = {}
    srcs = {}
    rxs = {}
    pmls = {}

    # To hold the maximum numerical ID for materials across multiple files
    material_ID_max = 0

    #################################################################
    # Read and display data from file(s), i.e. materials, sources,  #
    #                                           receivers, and PMLs #
    # Method depends on gprMax version                              #
    #################################################################

    for file in files:
        with open(file, 'rb') as f:
            #######################
            # Read data from file #
            #######################
            # Determine gprMax version
            # Read XML data
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            
            # Look for <gprMax> tag which indicates version <4
            try:
                xml_pos = mm.find(b'<gprMax')
                mm.seek(xml_pos)
                xml = mm.read(mm.size() - xml_pos)
                root = ET.fromstring(xml)
                # ET.dump(root)
                v4 = False
                print('\ngprMax version: < v.4.0.0')
                print(file)            
                # Read material names and numeric IDs into a dict
                for elem in root.findall('Material'):
                    materials[elem.get('name')] = int(elem.text)
                    if int(elem.text) > material_ID_max:
                        material_ID_max = int(elem.text)

                # Read sources
                for elem in root.findall('Sources'):
                    srcs[elem.get('name')] = int(elem.text)

                # Read receivers
                for elem in root.findall('Receivers'):
                    rxs[elem.get('name')] = int(elem.text)

                # Read PMLs
                for elem in root.findall('PML'):
                    pmls[elem.get('name')] = int(elem.text)

            except:
                v4 = True
                # Comments () embedded in line 3 of file
                f.readline()
                f.readline()
                c = f.readline().decode()
                # Strip comment tags
                c = c[5:-5]
                # Model information
                c = json.loads(c)
                print('\ngprMax version: ' + c['gprMax_version'])
                print(file)            

        ################
        # Display data #
        ################

        if v4:
            # Discretisation
            dl = c['dx_dy_dz']
            # Number of voxels
            nl = c['nx_ny_nz']

            # Store materials
            try:
                mats = c['Materials']
                for i, material in enumerate(mats):
                    materials[material] = i
                    if i > material_ID_max:
                        material_ID_max = i
            except KeyError:
                print('No materials to load')

            # Display any sources
            try:
                srcs = c['Sources']
                display_src_rx(srcs, dl)
            except KeyError:
                print('No sources to load')

            # Display any receivers
            try:
                rxs = c['Receivers']
                display_src_rx(rxs, dl)
            except KeyError:
                print('No receivers to load')

            # Display any PMLs
            try:
                pt = c['PMLthickness']
                display_pmls(pt, dl, nl)
            except KeyError:
                print('No PMLs to load')

        else:
            # Display any sources and PMLs
            srcs_pmls = dict(srcs)
            srcs_pmls.update(pmls)
            if srcs_pmls:
                for k, v in srcs_pmls.items():
                    threshold = threshold_filt(model, v, v, 'Sources_PML')
                    RenameSource(k, threshold)

                    # Show data in view
                    thresholddisplay = Show(threshold, renderview)
                    thresholddisplay.ColorArrayName = 'Sources_PML'
                    if v == 1:
                        thresholddisplay.Opacity = 0.5
                    threshold.UpdatePipeline()

            # Display any receivers
            if rxs:
                for k, v in rxs.items():
                    threshold = threshold_filt(model, v, v, 'Receivers')
                    RenameSource(k, threshold)

                    # Show data in view
                    thresholddisplay = Show(threshold, renderview)
                    thresholddisplay.ColorArrayName = 'Receivers'
                    threshold.UpdatePipeline()

    # Display materials
    material_range = range(0, material_ID_max + 1)
    for k, v in sorted(materials.items(), key=lambda x: x[1]):
        if v in material_range:
            threshold = threshold_filt(model, v, v, ['CELLS', 'Material'])
            RenameSource(k, threshold)

            # Show data in view, except for free_space
            if v != 1:
                thresholddisplay = Show(threshold, renderview)
                thresholddisplay.ColorArrayName = ['CELLS', 'Material']
            threshold.UpdatePipeline()


    RenderAllViews()

    # Reset view to fit data
    renderview.ResetCamera()

    # Show color bar/color legend
    # thresholdDisplay.SetScalarBarVisibility(renderview, False)

    # find source
    concrete = FindSource('concrete')

    # set active source
    SetActiveSource(concrete)

    # get color transfer function/color map for 'Material'
    materialLUT = GetColorTransferFunction('Material')

    # get opacity transfer function/opacity map for 'Material'
    materialPWF = GetOpacityTransferFunction('Material')

    # get 2D transfer function for 'Material'
    materialTF2D = GetTransferFunction2D('Material')

    # get display properties
    concreteDisplay = GetDisplayProperties(concrete, view=renderView1)

    # turn off scalar coloring
    ColorBy(concreteDisplay, None)

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(materialLUT, renderView1)

    # change solid color
    concreteDisplay.AmbientColor = [0.8274509803921568, 0.8274509803921568, 0.8274509803921568]
    concreteDisplay.DiffuseColor = [0.8274509803921568, 0.8274509803921568, 0.8274509803921568]

    # find source
    rebar = FindSource('rebar')

    # set active source
    SetActiveSource(rebar)

    # get display properties
    rebarDisplay = GetDisplayProperties(rebar, view=renderView1)

    # turn off scalar coloring
    ColorBy(rebarDisplay, None)

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(materialLUT, renderView1)

    # change solid color
    rebarDisplay.AmbientColor = [0.5019607843137255, 0.5019607843137255, 0.5019607843137255]
    rebarDisplay.DiffuseColor = [0.5019607843137255, 0.5019607843137255, 0.5019607843137255]

    # find source
    rebarcorrosion = FindSource('rebarcorrosion')

    # set active source
    SetActiveSource(rebarcorrosion)

    # get display properties
    rebarcorrosionDisplay = GetDisplayProperties(rebarcorrosion, view=renderView1)

    # turn off scalar coloring
    ColorBy(rebarcorrosionDisplay, None)

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(materialLUT, renderView1)

    # change solid color
    rebarcorrosionDisplay.AmbientColor = [0.7176470588235294, 0.2549019607843137, 0.054901960784313725]
    rebarcorrosionDisplay.DiffuseColor = [0.7176470588235294, 0.2549019607843137, 0.054901960784313725]

    # Properties modified on renderView1.AxesGrid
    renderView1.AxesGrid.Visibility = 0

    # Properties modified on renderView1
    renderView1.OrientationAxesVisibility = 0

    # get layout
    layout1 = GetLayout()

    # layout/tab size in pixels
    layout1.SetSize(1052, 834)

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [0.15000000596046448, 0.10000000149011612, 0.4762473672408525]
    renderView1.CameraFocalPoint = [0.15000000596046448, 0.10000000149011612, 0.0005000000237487257]
    renderView1.CameraParallelScale = 0.12313247929316902

    # save screenshot
    SaveScreenshot(f'{folder_path}/{folder}/{folder}_out.png', renderView1, ImageResolution=[1052, 834], 
        # PNG options
        CompressionLevel='0')

    #================================================================
    # addendum: following script captures some of the application
    # state to faithfully reproduce the visualization during playback
    #================================================================

    #--------------------------------
    # saving layout sizes for layouts

    # layout/tab size in pixels
    layout1.SetSize(1052, 834)

    #-----------------------------------
    # saving camera placements for views

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [0.15000000596046448, 0.10000000149011612, 0.4762473672408525]
    renderView1.CameraFocalPoint = [0.15000000596046448, 0.10000000149011612, 0.0005000000237487257]
    renderView1.CameraParallelScale = 0.12313247929316902

    #--------------------------------------------
    # uncomment the following to render all views
    # RenderAllViews()
    # alternatively, if you want to write images, you can use SaveScreenshot(...).

    print(f"Yay {folder}")

print("All folders processed.")