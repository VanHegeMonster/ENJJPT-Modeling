Current Software version: 27 Mar 2024
# UPT_Modeling
This program and code was created as part of Sheppard AFB, 80th FTW, A59 innovation team. The python code specifically takes the daily output from GTIMs and then cleans the daily files while also creating a composite to add for the A3S Data Tracker. The intent for this code is to add them to a Teams location and continually update there to ensure that Power BI applications pull the most current data while enabling future data processing and cross correlation among flights and individuals. 

This repo contains the base code and instructions for how to use the executible file processor to clean the files from GTIMs as well as directions for how to recompile and update the program in the future. On occassion, the software will be updated to account for bug fixes and changes due to GTIMs output. Please refer to the top line to ensure that your program is up-to-date with the most current push. 

- The general process for how this code works:
  1) User or script will download daily program files from GTIMs. (If a script, will need to confirm GTIMs access and OAuth access for Sharepoint access to a Teams Channel/Folder).
  2) These files will be placed in a folder that the python scripts knows to look for and process them accordingly. I.e. "Todays GTIMs Files"
  3) The processing will result in the creation of cleaned data tables which will be appended to existing tables which are located on a local OneDrive Instance. I.e. "DashBoard Source Files"
  4) OneDrive will sync those files to the cloud.
  5) Upon syncing those files to the cloud, the Power BI or _other platform_ will be able to access the refreshed data and provide the insights possibly on a daily level.

An example of the processed data for csvs will look like the following:
| Syllabus Days | Studs | Studs Complete | Flight Events | Avg Inc. | Inc. Days | Max Flight Events | Max Inc | Min Flight Events | Min Inc |
| ------------- | ----- | -------------- | ------------- | -------- | --------- | ----------------- | ------- | ----------------- | ------- |

### Changes to the Code
On occassion, changes within GTIMs and file permissions may require the adjustment of the code. Further, individuals seeking to ammend the code with feature adds are welcome to do so. The instructions for how to changes and recompile are below:
0 ) Ensure you have a computer with python (ideally Anaconda) installed.
1 ) After making changes to the script (recommend testing in Jupyter notebook for compatibility and testing of code), then run the following lines in an Anaconda Command Prompt. This step is recommended to reduce the overall file size of the executable file. In the Anaconda Command Prompt, run the following lines and adjust the directory as appropriate:
```
conda create --name myenv python=3.8
conda activate myenv
conda install tkinter os json datetime numpy pandas openpyxl
pip install pyinstaller [comment:note that in some instances, you may need to remove pathlib for pyinstaller to run appropriately]
cd path\to\your\script
```
Then, run pyinstaller:
Optional: ensure you have the upx executable file compiler to enhance the compression size of the compiler. \
If using upx, to create the executable file, use:
``` pyinstaller --onefile --windowed --upx-dir=/path/to/upx your_script.py ``` \
If not using upx:
``` pyinstaller --onefile --windowed File_Processor_Exe.py ``` 

Then, when the file is successfully compiled, use DoDSafe to provide the application to the users requiring its use. Note that to save it locally, users need to download it as a zip file from DoDSAFE and extract it prior to using the application. 

### Power BI:
Then, once the data is synced to the OneDrive and pulled as a link in PowerBI, Power BI will do the following:
1) Power BI intent is to create a Commander's Dashboard:\
1.a) Types of information to project:
- A3S Tracker Data and Graphs
- Ability to filter and segment by class/student
- When is the current class going to graduate?
- When is a student X going to graduate?
- How many students do you want yearly?
- How many CT sorties the squadron needs a year?
- Ask and see what additional data/functionality may be desired by the commanders\
Goal is to then have the data readily available – so it doesn’t take a week to pull it.\



 ## Modeling Thoughts (based on some brainstorming)
 A System Dynamics (SD) model for the pilot training pipeline would aim to capture the flow of students through the training program, accounting for various inputs and constraints. The goal is to understand how changes in these variables affect the capacity to train pilots and the optimal number of students per class. SD models excel in handling complex, feedback-driven systems, making them suitable for understanding how different factors interact over time.
#### Components of the SD Model
A SD model would include several key components, such as:
- Stocks: These are accumulations within the system, such as the number of students currently in training, instructors available, and aircraft ready for use.
- Flows: These represent the rates of change between stocks, such as students entering training, students completing or failing training, and instructors being allocated to classes or other duties.
- Feedback Loops: These are the cause-and-effect cycles that can either stabilize or destabilize the system. For example, a high attrition rate might lead to increasing the number of students per class, which could then affect the quality of training and further influence attrition rates.
- Delays: Time delays in the system, such as the time it takes for a student to progress through the training syllabus or attrition or other potential issues which can delay sortie generation.
#### Incorporating Monte Carlo Simulations
Monte Carlo simulations can be integrated into a System Dynamics model to handle uncertainty and variability in inputs, such as weather disruptions, maintenance issues, and refly rates. This approach allows one to run numerous simulations with inputs varied according to their probability distributions, leading to a range of possible outcomes. This is particularly useful for making probabilistic statements, like the chance of all students finishing on time given a certain class size.

#### Structure of the Model
1) Define the Syllabus Requirements: Start by outlining the training syllabus as a series of stages or milestones, each with associated probabilities of success, failure, and refly rates.
2) Model the Flow of Students: Create flows that represent students moving through the training syllabus, accounting for attrition and refly needs. This includes entering the pipeline, progressing through each stage, and either graduating or dropping out.
3) Incorporate Instructor and Aircraft Availability: Model the availability of instructors and aircraft as stocks that are depleted and replenished over time. Flows would represent the allocation of these resources to training sorties, impacted by additional duties, leave, and maintenance.
4) Integrate Feedback Loops and Delays: Include feedback mechanisms that capture how the system adjusts to changes, such as increases in class size affecting attrition rates or instructor availability influencing the number of operating days.
5) Run Monte Carlo Simulations: With the model structure in place, input distributions for uncertain variables can be defined (e.g., Gaussian distributions for weather disruptions or uniform distributions for refly rates). Running Monte Carlo simulations will then generate a spread of outcomes from which one can derive probabilities of interest, such as the likelihood of all students completing on time.
#### Outcome
The output of this model, enhanced with Monte Carlo simulations, would enable one to explore scenarios like:
"With X students per class, there's a 95% chance they will all finish on time, assuming a normal distribution of weather disruptions and a fixed rate of instructor availability."

### Simple Reminder for Stock and Flow Models 
Imagine a bathtub with a faucet that fills it with water (inflow) and a drain that lets water out (outflow). The level of water in the bathtub represents the "stock," while the faucet and drain represent the "flows."
- Stock: Water level in the bathtub
- Inflow: Water coming in from the faucet
- Outflow: Water going out through the drain
This system's dynamics can illustrate how changes in the inflow or outflow rates affect the stock (water level). Example python code below for this:
```
# Define the initial state and parameters
water_level = 0  # Initial water level in the bathtub (stock)
inflow_rate = 5  # Water flowing into the bathtub per minute (flow)
outflow_rate = 3  # Water flowing out of the bathtub per minute (flow)
simulation_time = 10  # Total time to simulate (minutes)

# Simulate the change in water level over time
for minute in range(simulation_time):
    water_level += inflow_rate  # Add the inflow
    water_level -= outflow_rate  # Subtract the outflow
    print(f"Minute {minute + 1}: Water Level = {water_level} liters")

# This simple loop models the stock (water level) changing over time due to the flows (inflow and outflow).
```
### Adpating this in a simpe progression for the current problem
Conceptual Model
- Stock: Current number of students in training.
- Inflow: New students entering the training program every X weeks.
- Outflow: Students graduating after completing their sorties.
Now, one needs to think about the numerous types of other variables which affect the tub and flow. What other stocks and flows affect this problem? What does a full picture of this look like?

### 3 Mar Modeling Thoughts
- There's a somewhat helpful video that sets up a good mental framework. Youtube link [here](https://www.youtube.com/watch?v=AnTwZVviXyY). One of the main takeaways is that: *Goals influence the Decisions we make, which then influence the state of the system as well as the the unintended consequences of our decisions which also affect the state of the system.* See 13:20 in the video for the diagram.
- Next, there's the discussion of the Fundamental Attribution Error: This is the error and the instinct to blame the people in the system rather than the system itself. Therefore, the modeling efforts will make the assumption that every student, IP, commander and staff member is intelligent, capable, and willing to put the effort in. That is, underflying or failure to produce students is not a by-product of the laziness of IPs.
- See slide deck [here](https://docs.google.com/presentation/d/1wr_SxpG1oxuaJ-70nTMbPOmFLafxikdDzaR6FNO-7Qc/edit?usp=sharing)
