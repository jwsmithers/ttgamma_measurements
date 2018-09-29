import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pylab import *
import numpy as np
from matplotlib import rc
import os
import matplotlib.pyplot as mpl

rc('text', usetex=True)
mpl.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath',               # <- tricky! -- gotta actually tell tex to use!
       r'\usepackage{amsmath}'
]  

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

var_names=["CDF", 
"ATLAS7_4", 
"ATLAS8",
"CMS_ljets",
"ATLAS13SL",
"ATLAS13DL"]

###################### 30_01_17 #######################
y_offset = 4.8
CDF={} 
CDF["total"]=[180, 14.58,-14.58]
CDF["lumi"]=[6]
CDF["theory"] = [170, +30, -30]
CDF["experiment"] = ["Tevetron, CDF"]
CDF["offset"] = [0,y_offset]
CDF["label"] = ["PRD 84 031104(R)\n"+r"$\sqrt{s}=1.96$~TeV"]

# Weird one
# ATLAS7={}
# ATLAS7["total"]=[2000, +860.0, -860.0]
# ATLAS7["lumi"]=[1.04]
# ATLAS7["theory"] = [2100, +400, -400]
# ATLAS7["experiment"]=["ATLAS"]
# ATLAS7["offset"] = [0,y_offset]
# ATLAS7["label"] = ["ATLAS-CONF-2011-153\n"+r"$\sqrt{s}=7$~TeV"]


# "Per lepton flavour??" 
ATLAS7_4={}
ATLAS7_4["total"]=[63, +18, -18]
ATLAS7_4["lumi"]=[4.59]
ATLAS7_4["theory"] = [48, +10, -10]
ATLAS7_4["experiment"]=["ATLAS"]
ATLAS7_4["offset"] = [-50,-y_offset-0.5]
ATLAS7_4["label"] = ["PRD 91 072007 (2015)\n"+r"$\sqrt{s}=7$~TeV"]


# CMS_fiducial={}
# CMS_fiducial["total"]=[127,+27,-27]
# CMS_fiducial["lumi"]=[19.7]
# CMS_fiducial["theory"]=[-999999, +1,-1]
# CMS_fiducial["experiment"]=["CMS"]
# CMS_fiducial["offset"] = [0,-y_offset]
# CMS_fiducial["label"] = ["JHEP 10 (2017) 006\n$\sqrt{s}=8$~TeV"] 
# It's the same one as above but for combined 
CMS_ljets={}
CMS_ljets["total"]=[515,+108.15,-108.15]
CMS_ljets["lumi"]=[19.7]
CMS_ljets["theory"]=[592, +77,-77]
CMS_ljets["experiment"]=["CMS"]
CMS_ljets["offset"] = [0,-y_offset-0.5]
CMS_ljets["label"] = ["JHEP 10 (2017) 006\n$\sqrt{s}=8$~TeV"] 

ATLAS8={}
ATLAS8["total"]=[139, +18.216, -18.216]
ATLAS8["lumi"]=[20.2]
ATLAS8["theory"] = [151, +24, -24]
ATLAS8["experiment"]=["ATLAS"]
ATLAS8["offset"] = [0,y_offset]
ATLAS8["label"] = ["JHEP 11 086 (2017)\n"+r"$\sqrt{s}=8$~TeV"]

ATLAS13SL={}
ATLAS13SL["total"]=[521, +41.9762, -41.9762]
ATLAS13SL["lumi"]=[36.1]
ATLAS13SL["theory"] = [495, +99, -99]
ATLAS13SL["experiment"]=["ATLAS"]
ATLAS13SL["offset"] = [0,-y_offset-0.5]
ATLAS13SL["label"] = ["ATLAS-CONF-2018-048\n"+ r"$\sqrt{s}=13$~TeV"]

ATLAS13DL={}
ATLAS13DL["total"]=[69, +5, -5]
ATLAS13DL["lumi"]=[36.1]
ATLAS13DL["theory"] = [63, +9, -9]
ATLAS13DL["experiment"]=["ATLAS"]
ATLAS13DL["offset"] = [-50,y_offset]
ATLAS13DL["label"] = ["ATLAS-CONF-2018-048\n"+ r"$\sqrt{s}=13$~TeV"]
ATLAS13DL["channel"] = "Dilepton"


# ATLAS13_inclusive={}
# ATLAS13_inclusive["total"]=[589, +35, -35]
# ATLAS13_inclusive["lumi"]=[36.1*1.1]
# ATLAS13_inclusive["theory"] = [558, +110, -110]
# ATLAS13_inclusive["experiment"]=["ATLAS"]
# ATLAS13_inclusive["offset"] = [-50,y_offset]
# ATLAS13_inclusive["label"] = [r"ATLAS-CONF-2018-048 ($\mathcal{L\times 1.1})$"+"\n"+ r"$\sqrt{s}=13$~TeV"]

channels={}
channels["CDF"]=CDF
channels["ATLAS7_4"]=ATLAS7_4
channels["ATLAS8"]=ATLAS8
channels["CMS_ljets"]=CMS_ljets
channels["ATLAS13SL"]=ATLAS13SL
channels["ATLAS13DL"]=ATLAS13DL

#channels["CMS_fiducial"]=CMS_fiducial


x=1.5 # Hard code this value for when the text right of the mu starts
rounding="{0:.3f}"
number_to_display = len(var_names)
height = number_to_display+3
bigFont=12
smallFont=11

################################################################################
# Set the basic canvas
fig = mpl.gcf()
fig.set_size_inches(7, 6)
ax = fig.add_subplot(111)
ax.xaxis.set_ticks_position("both")
ax.yaxis.set_ticks_position("both")
ax.tick_params(axis="y",which="both",direction = 'in')
ax.minorticks_on()
ax.tick_params(axis='x', which='both', direction='in')

plt.xlabel(r"Cross section [fb]", 
  horizontalalignment='right',x=1,fontsize=18)
plt.ylabel(r"Luminosity [fb$^{-1}$]",fontsize=18,horizontalalignment="left")

# plt.xscale('log')
plt.axis([0, 700,-4,55])
# plt.axis([1, 10000,-2,40])


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
    label = channels[var_names[i]]["label"][0]

    theory_nominal = abs(channels[var_names[i]]["theory"][0])
    theory_up = abs(channels[var_names[i]]["theory"][1])
    theory_down = abs(channels[var_names[i]]["theory"][2])
    theory_error=np.array([[theory_down],[theory_up]]) # Have to reverse it
    try:
      if channels[var_names[i]]["channel"] == "Dilepton":
        fillcolour=colour
    except KeyError:
        fillcolour="white"
    plt.errorbar(theory_nominal, y,xerr=theory_error, ecolor=colour,color=colour,marker="None",ms=7,
      elinewidth=20,capsize=0, alpha=0.4)
    plt.errorbar(mu, y,xerr=total_error, ecolor=colour,markeredgecolor=colour,color=fillcolour,marker="o",ms=6,
      elinewidth=3,capsize=5,zorder=1)

    plt.text(mu-x_label_offset,y+y_label_offset,label,
          fontsize=smallFont, color='black',va="center",horizontalalignment="center")
  draw_measurement()


atlas = mlines.Line2D([], [], color='b',linewidth=2.5, label=r'ATLAS')
cms = mlines.Line2D([], [], color='r',linewidth=2.5, label=r'CMS')
cdf = mlines.Line2D([], [], color='g',linewidth=2.5, label=r'Tevatron, CDF')
SL = mlines.Line2D([], [],marker="o", color='black',markersize=6,linewidth=0, label=r'Dilepton')
DL = mlines.Line2D([], [],marker="o", color='white',markeredgecolor="black",markersize=6,linewidth=0, label=r'Single lepton')

theory_uncert = mpatches.Patch(color='wheat', label='Theory uncertainty')

plt.tick_params(axis='both', which='major', labelsize=16)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.legend(handles=[atlas, cms,cdf,SL,DL,theory_uncert],loc=1,frameon=False,ncol=2,fontsize=12)

plt.show()
plt.savefig("measurements.eps", format="eps")
