# UPT_Modeling
This repo was created to help track changes for each commit and to help understand the changes to the code during each iteration as well as to recover potentially old versions of the code that may have been helpful. This is a private repo and access is only limited to those with a need to know and a need to code. Files should be saved locally to prevent leakage of data.

#### 24 Mar Update
- Successfully added instructions, error log, and more features to the GUI for operation.
- Tested the GUI out with example files and was able to get it to run with multiple files and of various programs.
- Note: Need to create the A3S Copy to file with the necessary data for last step.
- Work to reduce the dependencies required for running the code as an executable file.


#### 22 Mar Update
- Dashboard successfully amended to enable daily schedule refreshes at 1230 local.
- T6 student data looks good and filtering/slicing interactions have been fixed such that the table at the bottom is appropriate for all flights.
- Python code/test run of a .exe file on a government computer was successful. Some concerns lie ahead - in particular the concern regarding errors and debugging. This may mean that re-compliling the .exe file and re-DoD safeing it may be the only option. The current .exe does not enable users to edit the code. However, the GUI is able to show up and the code doesn't fail upon running. An additional concern is the shear size and start up of the compiler and file size. The script is fairly small, but apparently uses may dependencies. There may be some tinkering to make sure that many additional dependencies can be removed without breaking the program.
- Next steps:
  - Involve improving the flow and creating a .readme and instruction file for how to use the code
  - Creating extra buttons in the GUI for help and instructions.
  - Option for the GUI to amend code/provide directions for how to amend the code.
  - also spit out excel file with lined data to make the lives of the scheduling shop easier.

#### 11 Mar Update
- More work completed on reformatting the A3S tracker. Main data input sheets appear to be in a format that is likely conducive to more data processing programs and scripts.
- Some preliminary work on plotting in python to make sure that the data is legible and plotable. Conducted a bit of testing to see how the format of the xlsm file needs to be for simple decoding and ingesting.
- Approaching stage where the Power BI software is needed to thoroughly debug and refine the format for the tracker.
To dos for later:
- Will probably examine the coding of the GUI based on notes below.
- Testing of the .exe file to run and process scripts.

#### 7 Mar Update
- [x] Successfully created an initial GUI that's able to load files and run a "processing" script that puts them in a selected output folder.
Some additional	 features for the GUI that are under consideration
 - [ ] Creating an option for users to make exceptions for a specific call (i.e. T-6 24-08 has more syllabus days due to policy, but GTIM's doesn't report this.
 - [ ] Creating an output/terminal which conveys error messages when an error occurs.
 - [ ] Creating an option to enable users to open up the source code for the processing script
 - [ ] Creating a button which provides a README/instruction for how to use the program/what it does, where the github is and creating issue requests and so on.
Data processing notes:
- The A3S Tracker file needs to be updated and revised in a format that a computer can understand. A full review and understanding of the file is required ot make the changes such that python can read the input and update automatically... but more importantly, for the A3S Tracker file to be in a format that charts can be created from it and merged across multiple sheets.
	- Before testing in Power BI, this will need to be tested in Python to demonstrate feasibility.
 	- In addition, particular features of Power BI - which suggests more of a data splicing capability rather than a predictive capability means that prediction is rather going to be "pre-calculated". This also implies that data processing or another script is necessary in the future to conduct predictive analyses. 

#### 29 Feb Update
- Fixed the bug caused by missing data creating a misalignment in the data for new classes that don't have populated data.
- Fixed the automatic formating of Completed/Extra/Syllabus into a datetime format. (Kept it as a string)
- Talked to the Small Computer Shop to see the status of the Power BI software - TBD. Maybe... by next week?
- Working on how to integrate the data into a cloud/microsoft environment.
	- [x] I was successfully able to create a OneDrive instance on the local computer of the A5/9 Teams folder. This means a script can operate on local drives and save "locally" to the OneDrive which will automatically sync to the Teams website. This then could enable a user to update files which anyone with a Teams interface or link can access. **THIS IS A HUGE DEVELOPMENT**.
- Examined PyInstaller and py2exe. These both seem like promising choices, but more informaiton and testing is required of the original script to make sure that it will run consistently and work as intended.
- Considering general process for how this code will be used for future continuity:
  1) User or script will download daily program files from GTIMs. (If a script, will need to confirm GTIMs access and OAuth access for Sharepoint access to a Teams Channel/Folder).
  2) These files will be placed in a folder that the python scripts knows to look for and process them accordingly. I.e. "Todays GTIMs Files"
  3) The processing will result in the creation of cleaned data tables which will be appended to existing tables which are located on a local OneDrive Instance. I.e. "DashBoard Source Files"
  4) OneDrive will sync those files to the cloud.
  5) Upon syncing those files to the cloud, the Power BI or _other platform_ will be able to access the refreshed data and provide the insights possibly on a daily level.

Given these updates, the tasks for 1 Mar are as follows (will move up to the 1 Mar update after working):
- [ ] Adjust the script such that the code can incorporate numerous text files in a folder, and then write to and add to a csv. *Consider making a large CSV to test runtime for appending only to the end without reading it*
- [ ] Process the new files to add lines to the A3S tracker. Multiple options exist for this:
	- One option is to leave the file as is and print out the lines that should be copy/pasted into the file.
 	- The likely better alternative is to recreate the A3S file such that a computer can interpret the file and automatically append the rows. (Confirm with Greg to see if this is feasible.)
- [ ] Adjust version to better prepare it for running as a .py instead of a notebook.
- [ ] Look into GUI creation and functionality (what features would be needed?)

#### 28 Feb Update
Working on/Completed:\
- [X] [unchecked] Confirm that the code works with T38, IFF, and associated PIT tables.
	- [X] IFF
 		- [X] Note that a glitch was uncovered. GTIMs fails to output for the test files empty spaces: i.e. the text file won't maintain the structure with "X,Y,,Z", but rather "X,Y,Z". This mainly happens with new students.
   		- [X] Plan to fix is to reorient and rebuild the structure based based on what the size *should* be. A helpful marker perhaps is to use the "Completd / Extra / Syllabus" column to 'center' the data. This may work because that data is inherently textual and the structure of it is unique compared to all other entries and their formats.
- [X] Look into py2exe. This is a package that converts the python script into a computer executable (.exe) function. This then may allow users without python the ability to run and execute the script without needing python. Tests and functions for a GUI will be required to enable future long term usage.
	- [ ] (29 Feb Update) py2exe or pyInstaller are two different options. Given that the script location and the file location will likely vary over the iterations of LTs, there's likely a need to develop a GUI to help with those who don't have coding knowledge and to make it easier for reproducibility. 
- [X] Check the date format, 12/1/68 gets converted to 12/1/1968. It needs to remain a text input.
#### 27 Feb Update
Currently achieved:
- [x] Able to read GTIMs data and generate a cleaned Panadas dataframe.
- [x] Able to segment data based on class, student, flight and so on.
- [X] [Recheck 29 Feb] Confirm that the code works with T38, IFF, and associated PIT tables.
	- [X] T38
	- [X] [Updated again 29 Feb] IFF
	- [X] T6 PIT
	- [X] T38 PIT
	- [X] IFF PIT

Future Tasks and Considerations:
- [ ] Need to find a way to code it up and append to a large baseline table without needing to load the whole csv/sheet. Current information suggests the use of a csv file and csv_writer to update and add the lines. This would imply that for every new file input, use a script to ingest the data and write to csv file.
- [ ] Will need to experiment (pending Power BI desktop app), how quickly the files run. After 1 year, combined file size can start to get cumbersome ~10 MB. TBD on how significant this will be for slowing performance for end users.
	- [ ] Consider adding in a code snippit such that when a class is complete, it removes the class from the main file and saves the entire rest of the data to an archived file for just that class. This would ensure, that the commander's dashboard only contains active flying classes.
- [ ] An additional consideration is to create a GUI on my own. Would need to be something accessible by anyone on Teams/online. The online access will need the ability to porthole to Teams. (Probably best to keep it begrudgingly with PowerBI).
- [ ] Recreate the A3S file in a format that a computer can read (csv file). Take daily data and append to those files and rewrite those to a master Excel File. 

Required calculations that need to be included within the data:
- [ ] Updated graduation date (additional column)
	- [ ] Once data is ingested per day, calculate the projected graduation date for each student and therefore per class.
	- [ ] Be able to filter per student within each flight
- [ ] Calculate and present the data for the A3S table - Per class/program - calculate the following:

| Syllabus Days | Studs | Studs Complete | Flight Events | Avg Inc. | Inc. Days | Max Flight Events | Max Inc | Min Flight Events | Min Inc |
| ------------- | ----- | -------------- | ------------- | -------- | --------- | ----------------- | ------- | ----------------- | ------- |


This repo contains multiple tasks. One task involves the create of a systems dynamics model, and the other involves data processing raw GTIMs data for processing into a format for power BI.
### Power BI Tasks:
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
Reference the code [```Data Restructuring.ipynb```](https://github.com/VanHegeMonster/UPT_Modeling/blob/main/Data%20Restructuring.ipynb)

 ### Modeling Thoughts (based on some brainstorming)
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
