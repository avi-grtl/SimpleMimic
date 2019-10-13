import c4d.modules.character as c4dchar
import c4d.documents as c4ddoc
import c4d.utils as c4dutils
import c4d
import json

print "_____________"

body_desc = {
    "Skeleton": { "Joints": [], "BodyDefs": [], "DrawShapeDefs": [] }
}

# Recurses a hierarchy, starting from op
def recurse_hierarchy(op, parentID):
    global depth
    global globalID

    # print "{} parent: {}".format(depth, parentID)
    myID = parentID

    if isinstance(op, c4dchar.CAJointObject):

        globalID += 1
        myID = globalID

        pos = op.GetMl().off
        rot = c4dutils.MatrixToHPB(op.GetMl())

        body_desc["Skeleton"]["Joints"].append({
            "ID": myID,
            "Name": op.GetName(),
            "Type": "none",
            "Parent": parentID,
            "AttachX": round(pos.x, 5),
            "AttachY": round(pos.y, 5),
            "AttachZ": round(pos.z, 5),
            "AttachThetaX": round(rot.x, 5),
            "AttachThetaY": round(rot.y, 5),
            "AttachThetaZ": round(rot.z, 5),
            "LimLow0": -1.000000,
            "LimHigh0": 1.000000,
            "LimLow1": -1.000000,
            "LimHigh1": 1.000000,
            "LimLow2": -1.000000,
            "LimHigh2": 1.000000,
            "TorqueLim": 200,
            "IsEndEffector": 0,
            "DiffWeight": 1
        })
        body_desc["Skeleton"]["BodyDefs"].append({
            "ID": myID,
            "Name": op.GetName(),
            "Shape": "sphere",
            "Mass": 6.0,
            "ColGroup": 1,
            "EnableFallContact": 1,
            "AttachX": 0,
            "AttachY": 0,
            "AttachZ": 0,
            "AttachThetaX": 0,
            "AttachThetaY": 0,
            "AttachThetaZ": 0,
            "Param0": 10,
            "Param1": 10,
            "Param2": 10
        })
        body_desc["Skeleton"]["DrawShapeDefs"].append({
            "ID": myID,
            "Name": op.GetName(),
            "Shape": "sphere",
            "ParentJoint": myID,
            "AttachX": 0,
            "AttachY": 0,
            "AttachZ": 0,
            "AttachThetaX": 0,
            "AttachThetaY": 0,
            "AttachThetaZ": 0,
            "Param0": 10,
            "Param1": 10,
            "Param2": 10,
            "ColorR": 0.4706,
            "ColorG": 0.549,
            "ColorB": 0.6863,
            "ColorA": 1
        })
        # print "{} {} {} {}".format(depth, op.GetName(), myID, parentID)
    
    for child in op.GetChildren():
        depth += 1
        recurse_hierarchy(child, myID)
        depth -= 1

doc = c4ddoc.GetActiveDocument()
if doc:
    # Iterate all objects in the document
    depth = 0
    globalID = -1

    for op in doc.GetObjects():
        recurse_hierarchy(op, globalID)


with open("/Users/scott/Documents/deepmimic/DeepMimic/data/characters/agent.txt", "w") as f:
    printJson = json.dumps(body_desc, indent=4)
    f.write(printJson)
