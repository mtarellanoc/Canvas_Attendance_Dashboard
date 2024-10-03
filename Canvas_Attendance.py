import pandas as pd
import os
import hvplot.pandas
import panel as pn

download_directory = "C:\\Users\\mtare\\Downloads"

recent_file = ["", 0]
for file in os.listdir(download_directory):
    if file.endswith(".csv") and "attendance_reports_attendance" in file:
        file_directory = f"{download_directory}\\{file}"

        if os.path.getctime(file_directory) > recent_file[1]:
            recent_file = [file_directory, os.path.getctime(file_directory)]

df = pd.read_csv(recent_file[0], index_col=False)
df = df.drop(
    columns=["Course ID", "SIS Course ID", "Course Code", "Section Name", "Section ID", "SIS Section ID", "Teacher ID",
             "Teacher Name", "Timestamp"], axis=1)

course_name = df["Course Name"].loc[0]

# generating list of unique names and dates
names_list = []
dates_list = []
for i in range(len(df)):
    name = df["Student Name"].loc[i]
    date = df["Class Date"].loc[i]
    if name not in names_list:
        names_list.append(name)
    if date not in dates_list:
        dates_list.append(date)

names_list.sort()

# creating columns
df_columns = ["Full_Name", "Num_of_absences"]

for date in dates_list:
    df_columns.append(date)

# creating empty dataframe with columns
att_df = pd.DataFrame(columns=df_columns)

# filling dataframe with attendance and counting absences
i = 1
for student in names_list:
    row_data = [student]  # this list will be build with student, num of absences, and row_records

    row_records = []
    absent_counter = 0
    for date in dates_list:

        condition = (df["Student Name"] == student) & (df["Class Date"] == date)

        if df[condition].Attendance.empty:  # if attendance was not recorded on a particular date for a student
            row_records.append("n/a")
            absent_counter = absent_counter + 1

        else:
            for value in df[condition].Attendance:
                if value == "absent":
                    absent_counter = absent_counter + 1
                row_records.append(value)

    row_data.append(absent_counter)  # adding absent counter
    row_data.extend(row_records)  # extending row_data to include row_records

    att_df.loc[i] = row_data  # adding row of data to dataframe
    i = i + 1

table = att_df.hvplot.table(columns=df_columns, sortable=True, selectable=True, height=700)

# creating empty dataframe with columns
count_df = pd.DataFrame(columns = ["Date", "Students_Present"])

present_count = []  # present count by day

i = 1
for day in dates_list:
    row_data = []
    condition = (att_df[day] == "present")
    num_of_students = len(att_df[condition])
    row_data = [day, num_of_students]
    count_df.loc[i] = row_data  # adding row of data to dataframe
    i = i + 1

bargraph = count_df.hvplot.barh(y="Students_Present", x="Date",
                                responsive=True,
                                min_height=300,
                                min_width=300,

                                max_height=500,
                                max_width=500,
                                grid=True,
                                color="#9989e8"

                                )
bargraph

template = pn.template.EditableTemplate(
    editable=True,
    title=f"Attendance: {course_name}"
)
template.main.extend(
                    pn.Column(
                        pn.Row(table, bargraph)
                    )
)
template.show()