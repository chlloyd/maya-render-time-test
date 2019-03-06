import maya.cmds as cmds
import time
import os
import glob
import shutil

selectCam = "camera1"

workSpace = "Maya Project Folder Directory"

# [Camera AA, Diffuse Samples, Specular Samples, Transmission Samples, Subsurfce Scattering Samples, Indirect Volume Samples]
renderinput = [[3, 3, 4, 3, 4, 2], [5, 3, 4, 3, 4, 2], # Sample Settings
               [3, 5, 4, 3, 4, 2], [5, 5, 4, 3, 4, 2],
               [3, 3, 4, 5, 4, 2], [5, 3, 4, 5, 4, 2],
               [3, 5, 4, 5, 4, 2], [5, 5, 4, 5, 4, 2]]
			   

class mayaTimeRender():
    def __init__(self):
        allMesh = cmds.ls(type="mesh")
        for mesh in allMesh:
            cmds.setAttr(mesh+".aiSubdivType", 2)
            cmds.setAttr(mesh + ".aiSubdivIterations", 2)

        cmds.preferredRenderer("Arnold")
        cmds.setAttr("defaultResolution.width", 1920)
        cmds.setAttr("defaultResolution.height", 1080)
        cameras = cmds.ls(type="camera")

        for camera in cameras:
            if camera == selectCam:
                cmds.setAttr(selectCam + ".renderable", True)
            else:
                try:
                    cmds.setAttr(camera + ".renderable", False)
                except RuntimeError:
                    pass
        cmds.setAttr('defaultArnoldDriver.ai_translator', "tif", type='string')
        cmds.setAttr("defaultArnoldDriver.exrCompression", 2)
        cmds.setAttr("defaultRenderGlobals.outFormatControl", 0)
        cmds.setAttr("defaultRenderGlobals.animation", 0)
        cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)

    def setRenderAttributes(self, samplesList):
        cmds.setAttr("defaultArnoldRenderOptions.AASamples", samplesList[0])
        cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", samplesList[1])
        cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", samplesList[2])
        cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", samplesList[3])
        cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", samplesList[4])
        cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", samplesList[5])

    def renameLatestFile(self, newFilename):
        time.sleep(2)
        print(workSpace)
        list_of_files = glob.glob(workSpace + '/images/*.tif')
        print(list_of_files)
        latest_file = max(list_of_files, key=os.path.getctime).replace("\\", "/")
        print(latest_file)
        print(newFilename)
        shutil.move(latest_file, newFilename)

    def saveToFile(self, oneLine):
        resultsfile = open(workSpace+"/Render Results.txt", "a")
        resultsfile.write(oneLine)
        resultsfile.close()

    def render(self):
        for render in renderinput:
            self.setRenderAttributes(render)
            start_time = float(time.time())
            cmds.RenderSequence()
            finish_time = float(time.time())
            time_taken = round((finish_time - start_time),2)
            fileName = str(render[0]) + "." + str(render[1]) + "." + str(render[2]) + "." + str(render[3]) + "." + str(render[4]) + "." + str(render[5]) + ".tif"
            self.renameLatestFile(workSpace + "/images/completed/desk_scene." + fileName)
            self.saveToFile("Camera AA:"+str(render[0])+", Diffuse Samples:"+str(render[1])+", Specular Samples:"+str(render[2])+", Transmission Samples:"+str(render[3])+", SSS Samples:"+str(render[4])+", Volume Samples:"+str(render[5])+", Time Taken:"+str(time_taken)+" seconds\n")


timedRenders = mayaTimeRender()
timedRenders.render()