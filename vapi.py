import xml.etree.ElementTree as ET

tree = ET.parse('./apiproxy/proxies/default.xml')
root = tree.getroot()

count = 2
tscount = 0

def printStep(step):
    # Step is Policy, condition and faultrule
    # Lets get policy name first
    global count
    a = step.find('Name')
    if ((a is not None) and (a.text is not None)):
        # Remember this is the policy name, Let's get real name
        filename = "./apiproxy/policies/" + a.text + ".xml"
        tree = ET.parse(filename)
        root = tree.getroot()
        count = count + 1
        print(str(count) + "(" + root.tag + ":" + a.text + ") ", end = '')


    #a = step.find('FaultRules')
    #if ((a is not None) and (a.text is not None)):
    #    print(a.text)
    #a = step.find('Condition')
    #if ((a is not None) and (a.text is not None)):
    #    print("Condition: " + a.text)


def printRequest(req):
    # So request is basically a lot of steps
    for step in req:
        print(" -.-> ", end='')
        printStep(step)

def printResponse(resp):
    # So request is basically a lot of steps
    # Will have to print step in reverse order
    count=0
    stepback = []
    for step in resp:
#        if count == 0:
#            print(" --- | response |", end='')
#        else:
#            print(" --- ", end='')
        count = count+1
        stepback.append(step)
    while count > 0:
        print(" -- < --- ", end='')
        printStep(stepback.pop(count-1))
        count = count - 1
    print(" -- < --- " + str(tscount) + ">TargetServer]", end='')

def printCondition(cond):
    # Will have to modify text
    ns = cond.text.replace("\"","")
    print("-.-> " + str(count) + "{\"" + ns + "\"} ", end = '')


def printFlow(flow, respCpunt):
    global count
    global tscount
    # Possible options here are
    # Description, Request, Response, Condition
    #desc = flow.find('Description')
    req = flow.find('Request')
    resp = flow.find('Response')
    cond = flow.find('Condition')
    #if ((desc is not None) and (desc.text is not None)):
    #    print(desc.text)
    if (cond is not None):
        count = count + 1
        printCondition(cond)
        
    print("-.-> " + str(respCpunt) + "(" + flow.get("name") + ")", end = '')
    printRequest(req)
    if (tscount == 0):
        count = count + 1
        tscount = count
    print ("-.-> " + str(tscount) + ">TargetServer]")
    print("")
    print("\t" + str(respCpunt) + "(" + flow.get("name") + ")", end = '')
    printResponse(resp)
    print("")


# Start here
print('graph LR')
print("\t1[Client] ", end = '')
preflow = root.find('PreFlow')
printFlow(preflow,2)
count = count + 1

flows = root.find('Flows')
for fl in flows:
    print("\t1[Client] ", end = '')
    printFlow(fl,count)
    count = count +1
    # print(fl.tag)
    # print(fl.attrib)

count = count + 1
respCount = count
print("\t1[Client] ", end = '')
postflow = root.find('PostFlow')
printFlow(postflow,respCount)


#conn = root.find('HTTPProxyConnection')

