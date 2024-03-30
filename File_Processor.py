import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import datetime
import numpy as np
import pandas as pd

version_date = "27 Mar 2024"  # Example version date, adjust as needed


pd.set_option('display.max_rows', 90)
pd.set_option('display.max_columns', 55)
unit_columns = [
    'Unit', 'Effective Students', 'Remaining Flight Events', 'Remaining Device Events',
    'Remaining Academic Events', 'Days +/- Flights', 'Days +/- Devices', 'Days +/- Academics',
    'Days +/- Overall', 'Baseline / Day Flights', 'Baseline / Day Devices', 'Baseline / Day Academics',
    'Baseline / Day Overall', 'On-Track / Day Flights', 'On-Track / Day Devices', 'On-Track / Day Academics',
    'On-Track / Day Overall', 'Required / Day Flights', 'Required / Day Devices', 'Required / Day Academics',
    'Required / Day Total',
    'Date'
]
class_columns = [
    'Unit','Start Date','Graduation Date','Effective Students','Flight Days Remaining','Attrition Days Remaining',
    'Remaining Flight Events', 'Remaining Device Events','Remaining Academic Events', 
    'Days +/- Flights', 'Days +/- Devices', 'Days +/- Academics','Days +/- Overall', 
    'Baseline / Day Flights', 'Baseline / Day Devices', 'Baseline / Day Academics', 'Baseline / Day Overall',
    'On-Track / Day Flights', 'On-Track / Day Devices', 'On-Track / Day Academics','On-Track / Day Overall',
    'Healthy By Date','Healthy By Flights / Day','Healthy By Devices / Day','Healthy By Academics / Day','Healthy By Overall / Day',
    'Required / Day Flights', 'Required / Day Devices', 'Required / Day Academics','Required / Day Total',
    'Date'
]
individual_columns=[
    'Flight','Student','Last Flight Event','Last Flight Event Date','Last Device Event','Last Device Event Date','Primary Time','Night Time','Solo Time','Completd / Extra / Syllabus',
    'Remaining Flight Events', 'Remaining Device Events','Remaining Academic Events', 
    'Days +/- Flights', 'Days +/- Devices', 'Days +/- Academics','Days +/- Overall', 
    'Baseline / Day Flights', 'Baseline / Day Devices', 'Baseline / Day Academics', 'Baseline / Day Overall',
    'Date']
#     'Healthy By Flights / Day','Healthy By Devices / Day','Healthy By Academics / Day','Healthy By Overall / Day']

def realign_row_data(row, xyz_index_expected, total_columns):
    """
    Adjusts row data to ensure proper alignment, especially for the "X/Y/Z" formatted data,
    without unnecessarily extending the row beyond the expected total columns.
    """
    # Find the actual index of "X/Y/Z" formatted data
    xyz_actual_index = next((i for i, item in enumerate(row) if "/" in item and item.count("/") == 2), -1)
    
    # Initialize a new row with empty strings to ensure it has the correct structure
    new_row = [""] * total_columns
    
    # Keep the first two columns as they are always populated correctly
    new_row[0:2] = row[0:2]
    
    # Check if "X/Y/Z" formatted data is found and not in its expected position
    if 0 <= xyz_actual_index < len(row):
        # Shift data to align with the expected structure
        # Calculate shift amount; positive if "X/Y/Z" is before expected, negative if after
        shift = xyz_index_expected - xyz_actual_index
        
        # Apply shift and realign data, ensuring not to overflow the expected total columns
        for i, item in enumerate(row[2:], start=2):  # Skip the first two columns
            new_index = i + shift
            if 2 <= new_index < total_columns:  # Ensure within bounds, adjusting for the first two columns
                new_row[new_index] = item

    # Replace the original row with the realigned new row
    #Readjust the date
    new_row[-1]=row[-1]
    return new_row
def read_unit_summary_from_text(file_path):
    current_section = None
    unit_data = []
    class_data = []
    individual_data=[]
    skip_next_line = False  # Flag to skip the line following "TRAINING TIMELINE"
    # Flag to indicate if we are in the "Unit Summary" section
    in_unit_summary = False
    # List to hold the rows of the unit summary table
    exclusions = ['Unit', "*", "Baseline",'* Timeline','Remaining','Overall']  # Add any other patterns you wish to exclude
    with open(file_path, 'r') as file:
        i=0
        for line in file:
            # Skip line based on flag and then reset the flag
            if skip_next_line:
                skip_next_line = False
                Date=pd.to_datetime(line.strip('\n'),format='"%A, %B %d, %Y"') #Pull Day, Month Day, Year
    #             print(Date)
                continue

            if "TRAINING TIMELINE" in line:
    #             temp=current_section
                if current_section == None:
                    current_section = "Unit Summary"
                elif current_section == "Unit Summary":
                    current_section = "Class Summary"
                elif current_section == "Class Summary":
                    current_section = 'Individual Summary'
                skip_next_line = True  # Flag to skip the line following "TRAINING TIMELINE"
                print(current_section)
                continue

            #Add in exceptions:
            if any(exclusion in line for exclusion in exclusions):
                continue  # Skip this line and proceed to the next one
             # Condition to capture FLT value
            if current_section == 'Individual Summary' and 'FTS' in line:
                FLT = line.strip('\n')  # Assuming the entire line is what you want for FLT; adjust as needed
                continue
            # Split the line by comma and strip quotes/spaces
            row = [item.strip('\n').strip('"') for item in line.split(',')]

            # Prepend FLT to the row if needed
            if current_section == "Unit Summary":
                unit_data.append(row+[Date])
            elif current_section == "Class Summary":
                class_data.append(row+[Date])
            elif current_section=='Individual Summary':
                # Prepend FLT to the row if needed
                row.insert(0, FLT)
                row=[row[0],','.join(row[1:3])]+row[3:22]+[Date]
                row = realign_row_data(row, individual_columns.index('Completd / Extra / Syllabus'), len(individual_columns))

                #note that the row format is changed to DROP the Healthy By/Day columns due to data inconsistency by GTIMS
                individual_data.append(row)


    # Convert the captured data into pandas DataFrames
    unit_df = pd.DataFrame(unit_data, columns=unit_columns)  # Assuming first row is headers, adjust if not
    class_df = pd.DataFrame(class_data, columns=class_columns)  # Adjust as necessary
    individual_df = pd.DataFrame(individual_data, columns=individual_columns)  # Adjust as necessary
        
    #Treat this column as a string variable - ensures pandas doesn't read it as a date.
    individual_df['Completd / Extra / Syllabus'] = individual_df['Completd / Extra / Syllabus'].apply(lambda x: f"{x}")
    
    return unit_df, class_df, individual_df

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Processor")
        

        ## Setup notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.tab_main = ttk.Frame(self.notebook)  # Main tab
        self.notebook.add(self.tab_main, text='Main')
        
        self.tab_instructions = ttk.Frame(self.notebook)  # Instructions tab
        self.notebook.add(self.tab_instructions, text='Instructions')
        
        # self.notebook.add(self.tab_Code,text='Python Analysis Code')
                # Error log tab setup
        self.tab_error_log = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_error_log, text='Error Log')

        self.notebook.pack(expand=True, fill='both')


        ## Main Tab
        # Configure the grid for the main tab
        self.tab_main.grid_columnconfigure(1, weight=1)

        # Checkbox state variable
        self.save_folder_state = tk.IntVar(value=1)  # Default to checked, adjust based on settings later

        # Initialize GUI components on the main tab
        tk.Label(self.tab_main, text="Input File(s):").grid(row=0, column=0, sticky='nw')
        self.file_text = tk.Text(self.tab_main, height=1, width=60)
        self.file_text.grid(row=0, column=1, sticky='ew')
        tk.Button(self.tab_main, text="Browse...", command=self.browse_file).grid(row=0, column=2, sticky='nw')

        # Output folder setup on the main tab
        tk.Label(self.tab_main, text="Output Folder:").grid(row=1, column=0)
        self.folder_entry = tk.Entry(self.tab_main, width=60)
        self.folder_entry.grid(row=1, column=1, sticky='ew')
        tk.Button(self.tab_main, text="Browse...", command=self.browse_folder).grid(row=1, column=2, sticky='nw')

        # Checkbox for saving the output folder on the main tab
        self.save_folder_check = tk.Checkbutton(self.tab_main, text="Remember output folder", variable=self.save_folder_state)
        self.save_folder_check.grid(row=2, column=1, sticky='w')

        # Process button setup on the main tab
        tk.Button(self.tab_main, text="Process Files", command=self.process_files).grid(row=3, column=0, columnspan=3)
        # Load previous settings and adjust checkbox state
        self.load_settings()

        ## Instructions Tab
        # Instructions tab content setup
        self.instructions_text = tk.Text(self.tab_instructions, wrap='word', height=20, width=70)
        self.instructions_text.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(self.tab_instructions, command=self.instructions_text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.instructions_text.config(yscrollcommand=scrollbar.set)

        # Inserting instructions on instructions tab
        instructions_content = f"""
Last Version Update: {version_date}
Development Team: Sheppard AFB, 80th FTW, A5/9

This GUI is intended to help scheduling by automating the process of taking input from GTIMs and processing it such that the processed files can be stored in archives, enable better interpretation of the data format by computers for analysis, and to reduce the workload and burden of the hand-jamming process.

Instructions are below for how to use this program:
0. Ensure that you have the file path for the _Teams_ A3S tracker and associated data. The file path may look like "C/yourDoDIDHere/Teams/A59/SpecialProjects/PowerBIDashboard/". If you do not have this, refer to Microsoft instructions for syncing SharePoint and Teams files with your computer.
1. Download the daily report from GTIMs for each of the 6 programs in TEXT (.txt) file format [This will not work with other file types.] The file naming for this step doesn't matter, but we recommend a construct to prevent duplicates text files.
2. Use Browse button of the Input File(s) selector to add the 6 text files.
3. For first time use OR if Output folder field is not populated. Else, go to step 4. Use the Browse button of the Output folder to select the output folder. Again, we recommend using the Teams folder synced to your computer as this program first seeks to amend currently existing files. Check the box to remember output folder if desired.
4. Click Process Files. You should get a notification if files were processed successfully or if an error was thrown preventing the program from running. On occasion, the program may incorrectly process the files but successfully execute the code. It is worth checking and confirming on trial runs to make sure this works.
5. Open up the "A3S Tracker Additions.xlsx" and copy the lines to the appropriate sheets and classes in the file.
6. Ensure files are synced to Teams and call it a day!
"""
        self.instructions_text.insert('1.0', instructions_content)
        self.instructions_text.config(state='disabled')  # Make the text read-only

        # Bind the tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        ### Error Log Tab


        # Error log text widget with scrollbar
        self.error_log_text = tk.Text(self.tab_error_log, wrap='word', height=10, width=60)
        self.error_log_text.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        error_log_scrollbar = tk.Scrollbar(self.tab_error_log, command=self.error_log_text.yview)
        error_log_scrollbar.grid(row=0, column=1, sticky='ns')
        self.error_log_text.config(yscrollcommand=error_log_scrollbar.set)

        # Copy to Clipboard button
        self.copy_button = tk.Button(self.tab_error_log, text="Copy to Clipboard", command=self.copy_error_log_to_clipboard)
        self.copy_button.grid(row=1, column=0, sticky='w', padx=10, pady=5)

        # Clear Current Error Log button
        self.clear_button = tk.Button(self.tab_error_log, text="Clear Current Error Log", command=self.clear_error_log)
        self.clear_button.grid(row=1, column=0, sticky='e', padx=10, pady=5)

    def on_tab_changed(self, event):
        selected_tab = event.widget.select()  # Get the selected tab
        tab_name = event.widget.tab(selected_tab, "text")  # Get the name of the selected tab

        # Adjust the window size based on the selected tab
        if tab_name == "Main":
            self.root.geometry("700x300")  # Example size, adjust as needed
        elif tab_name == "Instructions":
            self.root.geometry("700x400")  # Adjust size for the Instructions tab content
        elif tab_name == "Error Log":
            self.root.geometry("700x300")  # Adjust size for the Instructions tab content
            
    def browse_file(self):
        filenames = filedialog.askopenfilenames(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        # Clear the Text widget and insert the selected file paths
        self.file_text.delete('1.0', tk.END)
        for filename in filenames:
            self.file_text.insert(tk.END, filename + '\n')
        # Adjust the height of the Text widget based on the number of files, up to a max of 6 lines
        line_count = min(len(filenames), 6)
        self.file_text.configure(height=line_count if line_count > 0 else 1)



    def browse_folder(self):
        foldername = filedialog.askdirectory()
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, foldername)

    def identify_program(self,class_df):
        program=''
        for item in class_df.Unit.unique():
            if '88 FTS' in item:
                program='IFF'
                if 'IS' in item:
                    program=program+"_PIT"
                break
            if "469" in item or "90" in item:
                program='T38'
                if "PIT" in item:
                    program=program+"_PIT"
                break
            if 'T-6' in item:
                program='T6'
                if "PIT" in item:
                    program=program+"_PIT"
                break
        return program

    def process_files(self):
        output_folder = self.folder_entry.get()  # Capture the output folder from the entry widget
    
        # Check if the output folder is blank
        if not output_folder.strip():
            messagebox.showerror("Error", "Output folder is required. Please specify an output folder.")
            return  # Exit the method early

        
        try:
            input_files = self.file_text.get('1.0', tk.END).strip().split('\n')
                # Initialize tracking for issues
            files_with_only_headers = []
            files_with_blank_cells = []
            
            # Save or delete the output folder setting based on the checkbox state
            if self.save_folder_state.get() == 1:
                self.settings['output_folder'] = output_folder
            else:
                self.settings.pop('output_folder', None)  # Safely remove the key if it exists
    
            self.save_settings()
    
            # Process each file
            if input_files:  # Check if the string is not empty
                for input_file in input_files:
                    
                     
                    # Place your file processing logic here
                    unit_df, class_df, individual_df = read_unit_summary_from_text(input_file)

                    # Identify the program based on class_df contents
                    program = self.identify_program(class_df)
                    # print(program)
                    
                    # Check for issues and track them
                    if any(len(df) <= 1 for df in [unit_df, class_df, individual_df]):
                        files_with_only_headers.append(input_file)
                    if any((df.replace('', np.nan).isnull()).any().any() for df in [unit_df, class_df, individual_df]):
                        files_with_blank_cells.append(input_file)
                    
                    A3SInputdf=[]
                    # [item.extract(r'\((.{5})') for item in class_df['Unit']]
                    # Step 1: Extract the desired substring from each cell in the column
                    extracted_series = class_df['Unit'].str.extract(r'\((.{5})')
                    
                    # Step 2: Get unique values from the extracted Series
                    unique_values = extracted_series[0].unique()
                    
                    # List to hold the rows for headers and data
                    rows_list = []
                    
                    for clas in unique_values:
                        # print(clas)
                        matching_rows_class = class_df.loc[class_df['Unit'].str.contains(f"\({clas}", regex=True)]
                        syllabus_days_remaining=pd.to_numeric(matching_rows_class['Flight Days Remaining'], errors='coerce').mean()
                        #create new df for single column due to multiple uses
                        effective_students_col=pd.to_numeric(matching_rows_class['Effective Students'], errors='coerce').sum()
                        effective_students=effective_students_col.sum()
                        studs_complete = (matching_rows_class['Remaining Flight Events'] == 0).sum()
                        flight_events_remaining=pd.to_numeric(matching_rows_class['Remaining Flight Events'], errors='coerce').sum()
                        
                        # Now go to the individual summaries for each class.
                        matching_rows_individuals = individual_df.loc[individual_df['Flight'].str.contains(f"\({clas}", regex=True)]
                        ind_flight_events_remaining_max=pd.to_numeric(matching_rows_individuals['Remaining Flight Events'], errors='coerce').max()
                        ind_flight_events_remaining_min=pd.to_numeric(matching_rows_individuals['Remaining Flight Events'], errors='coerce').min()
                        AvgInc=flight_events_remaining/effective_students/syllabus_days_remaining
                        IncDays=AvgInc*syllabus_days_remaining
                        MaxInc=ind_flight_events_remaining_max/syllabus_days_remaining
                        MinInc=ind_flight_events_remaining_min/syllabus_days_remaining
                        Date_Data_pulled=matching_rows_individuals.iloc[0].Date.strftime('%d-%b-%y')
                    
                        
                        
                        # Add the header row
                        header_row = [f'{clas} Syllabus Days', f'{clas} Studs', f'{clas} Studs Complete', 
                                      f'{clas} Flight Events', f'{clas} Avg Inc.', f'{clas} Inc. Days', 
                                      f'{clas} Max', f'{clas} Max Inc', f'{clas} Min', f'{clas} Min Inc', 
                                      f'{clas} Date Data Pulled']
                        rows_list.append(header_row)
                        
                        # Calculate your metrics for each class and add the data row
                        data_row = [syllabus_days_remaining, effective_students, studs_complete, flight_events_remaining,
                                    AvgInc, IncDays, ind_flight_events_remaining_max, MaxInc, 
                                    ind_flight_events_remaining_min, MinInc, Date_Data_pulled]
                        rows_list.append(data_row)
                    
                        #append to the larger existing dataframe
                    A3SInputdf = pd.DataFrame(rows_list)
                    sched_output_filepath=os.path.join(output_folder, f'{program}_Scheduling_output.xlsx')
                    with pd.ExcelWriter(sched_output_filepath) as writer:
                        A3SInputdf.to_excel(writer, sheet_name='A3SInputs', index=False)
                    ## Now move to the work for previous week student timeline slides (note that this is done per PROGRAM as opposed to per class):
                    if 'PIT' not in program:
                        # Execute code for student timeline slides
                        # 3. Under class summary, extract the columns for Unit, and Flight Days +/-
                        TimelineSlide_df=class_df[['Unit','Days +/- Flights']].copy()
                        
                        #To get the flying timeline data, go to the unit_df.
                        SummaryFlightsPM=unit_df.iloc[0]['Days +/- Flights']
                        SummaryReqdByDay=unit_df.iloc[0]['Required / Day Flights']
                        TimelineSlide_df.loc[len(TimelineSlide_df)] = ['Flying Timeline',SummaryFlightsPM]
                        TimelineSlide_df.loc[len(TimelineSlide_df)] = ['Sorties Reqd per Day',SummaryReqdByDay]
                        
                    
                            
                    
                        #Now for the student timeline summary
                        #Now for the student timeline summary
                        # Extract Effective Students, Flight Days +/-, and Overall Days +/-.
                        dummdf = unit_df[0:1].copy()
                        dummdf=dummdf[['Effective Students','Days +/- Flights','Days +/- Overall']].copy()
                        # step 4: Append to the dataframe for structure
                        dummdf['MDS']=program
                        
                        #Rearrange the columns
                        dummdf_cols=dummdf.columns.tolist()
                        dummdf_cols=dummdf_cols[-1:] + dummdf_cols[:-1]
                        dummdf_cols
                        dummdf=dummdf[dummdf_cols]
                        
                        # Next find the class that's going to graduate the soonest according to their syllabus:
                        # Step 1: Find the minimum number of flight days remaining
                        min_flight_days_remaining = class_df['Flight Days Remaining'].min()
                        
                        # Step 2: Filter the DataFrame to only include rows with this minimum value
                        rows_with_min_flight_days = class_df[class_df['Flight Days Remaining'] == min_flight_days_remaining]
                        
                        # Step 3: Find grad date and Timeline
                        soonest_grad_date=rows_with_min_flight_days['Graduation Date'][0]
                        soonest_grad_date_avg_daysPM=pd.to_numeric(rows_with_min_flight_days['Days +/- Flights']).mean()
                        
                        
                        # Add the 'Next Graduating Class' row
                        next_grad_row = pd.DataFrame([['Next Graduating Class', np.nan, np.nan, np.nan]],
                                                     columns=dummdf.columns)
                        
                        # Add the specific class with soonest graduation date row
                        # Note that clas should be defined in your context; replace it with the actual class identifier
                        specific_class_row = pd.DataFrame([[clas, effective_students, soonest_grad_date_avg_daysPM, soonest_grad_date]],
                                                          columns=dummdf.columns)
                        
                        # Concatenate the new rows to the original dummdf DataFrame
                        dummdf = pd.concat([dummdf, next_grad_row, specific_class_row], ignore_index=True)
                        
                        with pd.ExcelWriter(sched_output_filepath, mode='a') as writer:
                            TimelineSlide_df.to_excel(writer, sheet_name='Stud_Timeline_Slides', index=False)
                            dummdf.to_excel(writer, sheet_name='Stud_Timeline_Summary', index=False)




                                        
                    #Save files to csv
                    self.save_dfs_to_csv([unit_df, class_df, individual_df], program, output_folder)
                # After processing all files, display warnings if any issues were found
                if files_with_only_headers:
                    messagebox.showwarning("Warning", "The following files contain only headers or are empty, indicating input or processing errors:\n" + "\n".join(files_with_only_headers))
                if files_with_blank_cells:
                    messagebox.showwarning("Warning", "The following files contain one or more entirely blank cells, potentially indicating processing errors:\n" + "\n".join(files_with_blank_cells))
                # Show the message box to indicate completion
                messagebox.showinfo("Info", "Files processed successfully!")
            else:
                messagebox.showinfo("Info", "No Input Files!")
        except Exception as e:
            # Log the error in the error log tab
            self.DisplayExceptionError(e)

    def DisplayExceptionError(self,e):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        input_files = self.file_text.get('1.0', tk.END).strip()
        output_folder = self.folder_entry.get()
        print(e)
        error_message = f"Time: {current_time}\nVersion: {version_date}\nInput Files: {input_files}\nOutput Folder: {output_folder}\nError: {str(e)}\n\n"
        self.error_log_text.insert(tk.END, error_message)
        messagebox.showerror("Error", f"An error occurred:\n {e}.\n\n Please review the Error Log Tab. If you are unable to resolve this error, please contact Sheppard AFB A5/9")

    def save_dfs_to_csv(self,dfs, program, output_folder):
        filenames = {
            'individual': f'{program}_Individual_Data_DO_NOT_RENAME.csv',
            'unit': f'{program}_Summary_Data_DO_NOT_RENAME.csv',
            'class': f'{program}_Class_Data_DO_NOT_RENAME.csv'
        }
        
    
        for df_name, df in zip(filenames.keys(), dfs):
            try:
                file_path = os.path.join(output_folder, filenames[df_name])
    
                # Check if the output file already exists
                if os.path.exists(file_path):
                    # Read the existing data
                    # existing_df = pd.read_csv(file_path)
                    
                    # # Assuming 'Date' column exists in your DataFrame
                    # if 'Date' in df.columns:
                    #     new_dates = df['Date'].unique()
                    #     formatted_new_dates = {date.strftime('%Y-%m-%d') for date in new_dates}
                    #     existing_dates = existing_df['Date'].unique()
                        
                    #     # Check for any date in new data that already exists in the file
                    #     duplicate_dates = set(formatted_new_dates) & set(existing_dates)
                    #     if duplicate_dates:
                    #         # Inform the user about duplicates
                    #         # Desired output format
                    #         output_format = "%d %b %Y"
                    #         print(new_dates)
                    #         print(formatted_new_dates)
                    #         print(existing_dates)
                            
                    #         # Format each datetime object into the desired string format
                    #         formatted_dates = [date_obj for date_obj in duplicate_dates]

                    #         # Join the formatted date strings with a separator, e.g., ", "
                    #         formatted_dates_str = ", ".join(formatted_dates)
                            
                    #         # Use in the message box
                    #         messagebox.showwarning("Warning", f"Data may have already been added for these dates: {formatted_dates_str}. Please check the files for {file_path}.")
                    #         continue  # Skip saving this DataFrame
        
                    # Append new data if no duplicates are found
                    df.to_csv(file_path, mode='a', header=False, index=False)
                else:
                    # If the file doesn't exist, simply write the new DataFrame to a new file
                    df.to_csv(file_path, index=False)
            except Exception as e:
                print(file_path)
                df.to_csv(os.path.join(output_folder, "ERROR_FILE"+filenames[df_name]), index=False)
                self.DisplayExceptionError(e)

        

    
    def copy_error_log_to_clipboard(self):
        error_log = self.error_log_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(error_log)
        messagebox.showinfo("Info", "Error log copied to clipboard.")
    def clear_error_log(self):
        self.error_log_text.delete("1.0", tk.END)


    def load_settings(self):
        self.settings = {}
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        self.folder_entry.delete(0, tk.END)
        # Load the output folder if it was saved
        if 'output_folder' in self.settings:
            self.folder_entry.insert(0, self.settings['output_folder'])
            self.save_folder_state.set(1)
        else:
            self.save_folder_state.set(0)

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()