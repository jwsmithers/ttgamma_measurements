import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pylab import *
import numpy as np
from matplotlib import rc
import os
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)


################################################################################
def retrieve_fit_results(filename):
  with open(prefix+filename+".txt") as search:
      for line in search:
          line = line.rstrip()  # remove '\n' at end of line
          if "SigXsecOverSM" in line:
            fit_results = line.split()
  fit_results.pop(0)
  results = [float(i) for i in fit_results]

  try:
    with open(prefix+filename+"_statOnly.txt") as search:
        for line in search:
            line = line.rstrip()  # remove '\n' at end of line
            if "SigXsecOverSM" in line:
              print(line)
              fit_results_statOnly = line.split()
    fit_results_statOnly.pop(0)
    results_StatOnly = [float(i) for i in fit_results_statOnly]
  except IOError:
    print("WARNING: statOnly File not found")
    results_StatOnly = results


  return results, results_StatOnly


################################################################################

channel_names = ["Inclusive \n$\sqrt{s}=1.96$~TeV",
"Inclusive non-allhad \n$\sqrt{s}=7$~TeV", 
"$l+jets$ \n$\sqrt{s}=7$~TeV",
"$l+jets$ \n$\sqrt{s}=8$~TeV",
"Inclusive $\mu+jets$ \n$\sqrt{s}=8$~TeV",
"Inclusive $l+jets$ \n$\sqrt{s}=8$~TeV",
"Fiducial $l+jets$ \n$\sqrt{s}=8$~TeV",
]

var_names=["CDF", 
"ATLAS7",
"ATLAS7_4", 
"ATLAS8",
"CMS_mujets",
"CMS_ljets",
"CMS_fiducial"]

###################### 30_01_17 #######################
y_offset = 3
CDF={} 
CDF["total"]=[180, 14.58,-14.58]
CDF["lumi"]=[6]
CDF["theory"] = [170, +30, -30]
CDF["experiment"] = ["Tevetron, CDF"]
CDF["offset"] = [50,y_offset]

ATLAS7={}
ATLAS7["total"]=[2000, +860.0, -860.0]
ATLAS7["lumi"]=[1.04]
ATLAS7["theory"] = [2100, +400, -400]
ATLAS7["experiment"]=["ATLAS"]
ATLAS7["offset"] = [100,y_offset]


ATLAS7_4={}
ATLAS7_4["total"]=[63000, +17010.0, -17010.0]
ATLAS7_4["lumi"]=[4.59]
ATLAS7_4["theory"] = [48000, +10000, -10000]
ATLAS7_4["experiment"]=["ATLAS"]
ATLAS7_4["offset"] = [30000,y_offset]


CMS_mujets={}
CMS_mujets["total"]=[2400,+631.2,-631.2]
CMS_mujets["lumi"]=[19.7]
CMS_mujets["theory"]=[1800, +500,-500]
CMS_mujets["experiment"]=["CMS"]
CMS_mujets["offset"] = [100,y_offset]


CMS_ljets={}
CMS_ljets["total"]=[515,+108.15,-108.15]
CMS_ljets["lumi"]=[19.7]
CMS_ljets["theory"]=[591, +77,-77]
CMS_ljets["experiment"]=["CMS"]
CMS_ljets["offset"] = [100,y_offset]


CMS_fiducial={}
CMS_fiducial["total"]=[127,+27,-27]
CMS_fiducial["lumi"]=[19.7]
CMS_fiducial["theory"]=[-999999, +1,-1]
CMS_fiducial["experiment"]=["CMS"]
CMS_fiducial["offset"] = [52,-y_offset]


ATLAS8={}
ATLAS8["total"]=[139, +18.216, -18.216]
ATLAS8["lumi"]=[20.2]
ATLAS8["theory"] = [151, +24, -24]
ATLAS8["experiment"]=["ATLAS"]
ATLAS8["offset"] = [43,y_offset]

channels={}
channels["CDF"]=CDF
channels["ATLAS7"]=ATLAS7
channels["ATLAS7_4"]=ATLAS7_4
channels["ATLAS8"]=ATLAS8
channels["CMS_mujets"]=CMS_mujets
channels["CMS_ljets"]=CMS_ljets
channels["CMS_fiducial"]=CMS_fiducial


x=1.5 # Hard code this value for when the text right of the mu starts
rounding="{0:.3f}"
number_to_display = len(channel_names)
height = number_to_display+3
bigFont=12
smallFont=9
################################################################################


# Set the basic canvas
plt.xlabel(r"Cross section [fb]", 
  horizontalalignment='right',x=1)
plt.ylabel(r"Luminosity [fb$^{-1}$]")

#plt.yticks([])
# plt.axvline(x=1,linewidth=2, color='k',linestyle="--")
# plt.axhline(y=2, linewidth=1, color='grey', linestyle='-')
# plt.axhline(y=4, linewidth=1, color='grey', linestyle='-')

plt.xscale('log')
plt.axis([50, 150000,-2,35])
# plt.axis([1, 10000,-2,40])

# plt.text(0.08,height-0.8,r"\textit{\textbf{ATLAS}} internal",
#           fontsize=18, color='black')
# plt.text(0.08,height-1.5,r"$\sqrt{s}=13$~TeV, 36.1, fb$^{-1}$",
#           fontsize=14, color='black')
# plt.text(x+0.4,height-2.85,r"\textbf{Total}   (sys   stat)",
#           fontsize=10, color='black',va="center")
plt.legend(loc=1)


# # merged and 2mu text
# plt.text(0.1,1,r"\emph{2-$\mu$}",
#           fontsize=10, color='black',va="center",rotation="vertical")
# plt.text(0.1,3,r"\emph{merged}",
#           fontsize=10, color='black',va="center",rotation="vertical")

# Loop over the user defined channels
for i in range(0, len(var_names)):
  def draw_measurement():
    mu = channels[var_names[i]]["total"][0]
    total_up = abs(channels[var_names[i]]["total"][1])
    total_down = abs(channels[var_names[i]]["total"][2])
    total_error=np.array([[total_down],[total_up]]) # Have to reverse it


    #y=i+0.5
    y = abs(channels[var_names[i]]["lumi"][0])
    experiment=channels[var_names[i]]["experiment"][0]
    if experiment == "ATLAS":
      colour="b"
    elif experiment == "CMS":
      colour="r"
    else: 
      colour="g"

    y_label_offset=channels[var_names[i]]["offset"][1]
    x_label_offset=channels[var_names[i]]["offset"][0]

    theory_nominal = abs(channels[var_names[i]]["theory"][0])
    theory_up = abs(channels[var_names[i]]["theory"][1])
    theory_down = abs(channels[var_names[i]]["theory"][2])
    theory_error=np.array([[theory_down],[theory_up]]) # Have to reverse it
    plt.errorbar(theory_nominal, y,xerr=theory_error, ecolor=colour,color=colour,marker="None",ms=7,
      elinewidth=30,capsize=0, alpha=0.4)
    plt.errorbar(mu, y,xerr=total_error, ecolor=colour,color=colour,marker="o",ms=7,
      elinewidth=3,capsize=5)

    plt.text(mu-x_label_offset,y+y_label_offset,r" "+channel_names[i],
          fontsize=smallFont, color='black',va="center")
  draw_measurement()


stat = mlines.Line2D([], [], color='b',linewidth=2.5, label=r'ATLAS')
total = mlines.Line2D([], [], color='r',linewidth=2.5, label=r'CMS')
theory_uncert = mpatches.Patch(color='wheat', label='theory')

plt.legend(handles=[total, stat, theory_uncert],loc=1,frameon=False)

plt.show()
plt.savefig("measurements.pdf")
