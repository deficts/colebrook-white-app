import math

MAX_ITER=1000000

def modifiedFalsePosition(diameter,roughness,reynolds):
    a = .008
    b = .08
    def colebrook(f):
        return (1/f**0.5)+2.0*(math.log10(2.51/(reynolds * f**0.5)+(roughness/1000)/(3.72*diameter)))
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

def ColebrookWhite(velocity,diameter,roughness,density,viscosity):
    velocity=float(velocity)
    diameter = float(diameter)/1000
    roughness = float(roughness)
    density = float(density)
    viscosity = float(viscosity)
    reynolds = velocity*diameter*density/viscosity
    return modifiedFalsePosition(diameter,roughness,reynolds)
