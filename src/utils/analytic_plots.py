import matplotlib.pyplot as plt
# import numpy as np

default_timedomain_texts = {"y_legend":"$y(t)$",
                            "title": "Time-domain plot",
                            "y_label": "$y(t)$",
                            "x_label": "time [ms]"
                            }

def timedomain_plot(figaxis,x,y,**kwargs):
    if "y_legend" in kwargs["texts"]:
        figaxis.plot(x, y, '-k', label=kwargs["texts"]["y_legend"])
    else:
        figaxis.plot(x, y, '-k')

    if "title" in kwargs["texts"]:
        plt.title(kwargs["texts"]["title"], loc='left')

    if "y_label" in kwargs["texts"]:
        figaxis.set_ylabel(kwargs["texts"]["y_label"])

    if "x_label" in kwargs["texts"]:
        figaxis.set_xlabel(kwargs["texts"]["x_label"])

    figaxis.grid(True)
    lgd = figaxis.legend(loc='upper right', bbox_to_anchor=(1.12, 1.35))
    if "axes" in kwargs:
        figaxis.axis(kwargs["axes"])