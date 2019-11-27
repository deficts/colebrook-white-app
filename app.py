from flask import Flask, render_template, flash, redirect, url_for, session, request
from pipes import ColebrookWhite
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

cw=0

class pipeData:
    def __init__(self,velocity,diameter,roughness,density,viscosity):
        self.velocity=velocity
        self.diameter=diameter
        self.roughness=roughness
        self.density=density
        self.viscosity=viscosity

@app.route('/')
def index():
    pipe=None
    return render_template('index.html',pipe=pipe)

@app.route('/', methods=['POST'])
def index_post():
    if(request.method=='POST'):
        pipe = pipeData(request.form['Velocity'],request.form['Diameter'],request.form['Roughness'],request.form['Density'],request.form['Viscosity'])
        cw=ColebrookWhite(pipe.velocity,pipe.diameter,pipe.roughness,pipe.density,pipe.viscosity)
        PlotColebrook(pipe.velocity,pipe.diameter,pipe.roughness,pipe.density,pipe.viscosity)
    return render_template('index.html', pipe=pipe, cw=cw)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def PlotColebrook(velocity,diameter,roughness,density,viscosity):
    plt.cla()
    velocity=float(velocity)
    diameter = float(diameter)/1000
    roughness = float(roughness)
    density = float(density)
    viscosity = float(viscosity)
    reynolds = velocity*diameter*density/viscosity
    def colebrook(f):
        return (1/np.sqrt(f))+2.0*(np.log10(2.51/(reynolds * np.sqrt(f))+(roughness/1000)/(3.72*diameter)))
    x=np.arange(.008,.08,.01)
    vecfunc=np.vectorize(colebrook)
    t=vecfunc(x)
    plt.plot(x,t)
    plt.show(block=False)
    plt.savefig('static/new_plot.png')

if __name__=='__main__':
    app.run(debug=True)
