import math

MAX_ITER=1000000

while True: #Quick Error Checking. Will need to convert into function that also checks for non-negative as well as defaults and can be applied against all variables.
    try:
        velocity = float(input("Please enter velocity in m/s "))
    except ValueError:
        print("Velocity must be a number")
        continue
    else:
        break
while True:
    try:
        diameter = float(input("Please enter Pipe Internal Diameter in mm: "))
    except ValueError:
        print("Pipe diameter must be a number.")
        continue
    else:
        break
roughness = input("please enter Material Roughness in mm [HDPE: 0.007]: ")
density = input("Please enter Fluid Density in kg/m3 [Water @ 20C: 998]: ")
viscosity = input("Please enter Fluid Viscosity in Pa.s [Water @ 20C: 0.001]: ")

if not roughness:
    roughness = 0.007   #Default HDPE
if not density:
    density = 998       #Default Ddensity of water @ 20C
if not viscosity:
    viscosity = 0.001   #Default Viscosty of Water @ 20C

#Turn all values into floating points
diameter = float(diameter)/1000
roughness = float(roughness)
density = float(density)
viscosity = float(viscosity)


pipearea = float(diameter**2 / 4 * math.pi) #Pipe Area in m^2

reynolds = velocity*diameter*density/viscosity # Reynolds Number for Full Circular Pipe

def modifiedFalsePosition(diameter,roughness,reynolds):
    a = .008
    b = .08
    if colebrook(a)*colebrook(b)>=0 :
        return -1
    c=a
    for i in range(MAX_ITER):
        c=(a*colebrook(b)-b*colebrook(a))/(colebrook(b)-colebrook(a))
        if colebrook(c) == 0:
            break
        elif colebrook(c)*colebrook(a) < 0:
            b=c
        else:
            a=c
    return c

def colebrook(f):
    return (1/f**0.5)+2.0*(math.log10(2.51/(reynolds * f**0.5)+(roughness/1000)/(3.72*diameter)))

def SwameeJain(diameter, roughness, reynolds):
    return 0.25 / (math.log10((roughness/1000)/(3.7*diameter)+5.74/(reynolds**0.9)))**2

def CalculateHL(friction,velocity,diameter):
    return 100 * friction * 1 / (2*9.81) * velocity**2/diameter

CWFriction = modifiedFalsePosition(diameter,roughness,reynolds)
SJFriction = SwameeJain(diameter,roughness,reynolds)

#Print results in nice 'table'
print("\n---------------RESULTS----------------")
print("Reynolds Number\t|\t{:.0f}".format(reynolds))
print("Pipe Area \t|\t{:.0f}\t(mm^2)".format(pipearea*1000**2))
print("Velocity \t|\t{:.2f}\t(m/s)".format(velocity))
print("------------FRICTION FACTOR-----------")
print("Colebrook-White\t|\t{:.4f}".format(CWFriction))
print("Swamee-Jain\t|\t{:.4f}".format(SJFriction))
print("--------FRICTION LOSS PER 100M--------")
print("Colebrook-White\t|\t{:.2f}".format(CalculateHL(CWFriction,velocity,diameter)))
print("Swamee-Jain\t|\t{:.2f}".format(CalculateHL(SJFriction,velocity,diameter)))
