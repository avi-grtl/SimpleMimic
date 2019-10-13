
import c4d.modules.character as c4dchar
import c4d.documents as c4ddoc
import c4d.utils as c4dutils
import c4d
import json

print "_____________"

anim_desc = {
    "Loop": "wrap",
    "Frames": []
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
        
        if myID == 0: # if root, add offset pos
            pos = op.GetMl().off
            anim_desc["Frames"][-1].append(.5)
            anim_desc["Frames"][-1].append(round(pos.x, 5))
            anim_desc["Frames"][-1].append(round(pos.y, 5))
            anim_desc["Frames"][-1].append(round(pos.z, 5))

        # only add quaternions
        rot = c4dutils.MatrixToHPB(op.GetMl())
        q = c4d.Quaternion()
        q.SetHPB(rot)
        anim_desc["Frames"][-1].append(round(q.w, 5))
        anim_desc["Frames"][-1].append(round(q.v.x, 5))
        anim_desc["Frames"][-1].append(round(q.v.y, 5))
        anim_desc["Frames"][-1].append(round(q.v.z, 5))

    for child in op.GetChildren():
        depth += 1
        recurse_hierarchy(child, myID)
        depth -= 1

doc = c4ddoc.GetActiveDocument()
if doc:
    # Iterate all objects in the document
    depth = 0
    globalID = -1

    anim_desc
    anim_desc["Frames"].append([])
    for op in doc.GetObjects():
        recurse_hierarchy(op, globalID)


with open("/Users/scott/Documents/deepmimic/DeepMimic/data/motions/agent.txt", "w") as f:
    printJson = json.dumps(anim_desc, indent=4)
    f.write(printJson)