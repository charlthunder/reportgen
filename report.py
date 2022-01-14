from tkinter import Tk, Label, Button, StringVar, Entry
import pymysql
import pandas as pd
from fpdf import FPDF


class ReportGenerator:
    title = 'Axium Education: Termly Report'

    def __init__(self, master):

        self.master = master
        master.title("Report Generator")

        # Labelgenerator
        def labelmaker(text):
            self.label_text = StringVar()
            self.label_text.set(text)
            self.label = Label(master, textvariable=self.label_text)
            self.label.pack()

        # SCHOOL
        labelmaker('School')
        self.schoolentry = Entry(master)
        self.schoolentry.pack()

        # GRADE
        labelmaker('Grade')
        self.gradeentry = Entry(master)
        self.gradeentry.pack()

        # YEAR
        labelmaker('year')
        self.yearentry = Entry(master)
        self.yearentry.pack()

        # TERM
        labelmaker('Term')
        self.termentry = Entry(master)
        self.termentry.pack()

        # BUTTON TO GENERATE REPORT
        self.greet_button = Button(master, text="Termly Report", command=self.i_printreport)
        self.greet_button.pack()

        self.week_button = Button(master, text="Weekly Report", command=self.w_printreport)
        self.week_button.pack()

        # BUTTON TO CLOSE REPORT
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    # Print individual report
    def i_printreport(self):
        self.i_makepdf(self.schoolentry.get(), self.gradeentry.get(), self.yearentry.get(), self.termentry.get())

    # Print school report
    def s_printreport(self):
        self.s_makepdf(self.schoolentry.get(), self.gradeentry.get(), self.yearentry.get(), self.termentry.get())

    # Print weekly report
    def w_printreport(self):
        self.w_makepdf(self.schoolentry.get(), self.gradeentry.get(), self.yearentry.get(), self.termentry.get())

    # Call individual pdf
    def i_makepdf(self, school, grade, year, term):
        pdf = i_PDF()
        pdf.getentries(school, grade, year, term)
        pdf.set_title(self.title)
        pdf.set_author('Axium Education')
        pdf.print_chapter(f'{school}', f'{grade}', f'{year}', f'{term}')
        pdf.output(f'{school}_{grade}.pdf', 'F')

    # Call school pdf
    def s_makepdf(self, school, grade, year, term):
        pdf = s_PDF()
        pdf.getentries(school, grade, year, term)
        pdf.set_title(self.title)
        pdf.set_author('Axium Education')
        pdf.print_chapter(f'{school}', f'{grade}', f'{year}', f'{term}')
        pdf.output(f'{school}_{grade}.pdf', 'F')

    def w_makepdf(self, school, grade, year, term):
        pdf = w_PDF()
        pdf.getentries(school, grade, year, term)
        pdf.set_title(self.title)
        pdf.set_author('Axium Education')
        pdf.print_chapter(f'{school}', f'{grade}', f'{year}', f'{term}')
        pdf.output(f'{school}_{grade}_w.pdf', 'F')


class i_PDF(FPDF):

    # school = ''
    # grade = ''
    # year = ''
    # term = ''

    def getentries(self, school, grade, year, term):
        self.school = school
        self.grade = grade
        self.year = year
        self.term = term

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(ReportGenerator.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 165, 0)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, 'Axium Education: Termly Report', 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, name, grade, year, term):
        # Arial 12
        self.set_font('Arial', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, f'{name} {year} - Grade {grade}', 0, 1, 'L', 1)
        self.cell(0, 6, f'Term: {term}', 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, school, grade, year, term):

        # Connect to server
        cn = pymysql.connect(host='10.1.1.2', user='root', password='<Insert>', db='axium')

        # Grab ekuk attendance
        ekuk_aten = pd.read_sql("SELECT students.student_id as student_id, students. firstname, students.lastname, round((count(IF(attended = 1, true, NULL)) / count(*))*100, 2) as percentageAttended, round((count(IF(attended = 2, true, NULL)) / count(*))*100,2) as percentageExcused, round((count(IF(attended = 0, true, NULL)) / count(*))*100,2) as percentageNotAttended FROM attendance JOIN enrollment ON attendance.student_id = enrollment.student_id JOIN classes ON attendance.class_id = classes.class_id JOIN students ON attendance.student_id = students.student_id WHERE EXTRACT(YEAR FROM classes.date) = '{}' AND QUARTER(classes.date) = {} AND  enrollment.program = 'Ekukhuleni' AND classes.class_type = 'Saturdays' AND enrollment.end is NULL AND students.current_school = '{}' AND students.current_grade = {} GROUP BY students.student_id ORDER BY students.lastname;".format(year, term, school, grade), con=cn)
        ekuk_aten.set_index('student_id', inplace=True)

        # Grab SG attendance
        SG_aten = pd.read_sql("SELECT students.student_id, students. firstname, students.lastname, round((count(IF(attended = 1, true, NULL)) / count(*))*100, 2) as percentageAttended, round((count(IF(attended = 2, true, NULL)) / count(*))*100,2) as percentageExcused, round((count(IF(attended = 0, true, NULL)) / count(*))*100,2) as percentageNotAttended FROM attendance JOIN enrollment ON attendance.student_id = enrollment.student_id JOIN classes ON attendance.class_id = classes.class_id JOIN students ON attendance.student_id = students.student_id WHERE EXTRACT(YEAR FROM classes.date) = '{}' AND QUARTER(classes.date) = {} AND  enrollment.program = 'Ekukhuleni' AND classes.class_type = 'Study Groups' AND enrollment.end is NULL AND students.current_school = '{}' AND students.current_grade = {} GROUP BY students.student_id ORDER BY students.lastname;".format(year, term, school, grade), con=cn)
        SG_aten.set_index('student_id', inplace=True)

        # Grab Assessment info
        assess = pd.read_sql("SELECT students.student_id, ax_tests.date, ax_tests.subject,students.current_school, students.firstname, students.lastname, tests.grade, tests.term, ax_tests.comment, round((tests.mark/ax_tests.mark)*100,2) as mark FROM ax_tests JOIN tests ON ax_tests.test_id = tests.test_id JOIN students ON tests.student_id = students.student_id JOIN enrollment ON students.student_id = enrollment.student_id WHERE EXTRACT(YEAR FROM ax_tests.date)='{}' AND enrollment.program = 'Ekukhuleni' AND ax_tests.term = {} AND students.current_school='{}' AND ax_tests.grade = {} ORDER by students.student_id ;".format(year, term, school, grade), con=cn)

        # The averages do not require index
        assessave = assess

        # The rest requires student_id to be the index
        assess.set_index('student_id', inplace=True)


        # Variables to check aid in adding new pages
        counter = 0
        maxs = len(ekuk_aten.index)

        # Class average
        classave = assessave.groupby(['subject']).mark.mean().reset_index().round(2)
        mathclassave = classave['mark'][classave['subject'] == 'Mathematics']
        englishclassave = classave['mark'][classave['subject'] == 'English']
        psclassave = classave['mark'][classave['subject'] == 'Physical Sciences']

        mathclassave = mathclassave.to_string(index=False, header=False)
        englishclassave = englishclassave.to_string(index=False, header=False)
        psclassave = psclassave.to_string(index=False, header=False)

        # print(classave)
        # print(mathclassave)
        # print(englishclassave)
        # print(psclassave)


        # Run through every student ID to find respective saturday attendance, study groups attendance and assessment data
        for sid in ekuk_aten.index:
            # Try to locate the student ID, If there is no such student ID, skip. It means the student was not yet enrolled in that term
            try:
                counter = counter + 1
                firstname = ekuk_aten.loc[sid, ['firstname']]
                lastname = ekuk_aten.loc[sid, ['lastname']]

                # Transform into correct data type
                firstname = firstname.head(1).to_string(index=False, header=False)
                lastname = lastname.head(1).to_string(index=False, header=False)

                # Ekukhuleni -----------------------
                attendedE = ekuk_aten.loc[sid, ['percentageAttended']]
                attendedE = attendedE.head(1).to_string(index=False, header=False)

                notattendedE = ekuk_aten.loc[sid, ['percentageNotAttended']]
                notattendedE = notattendedE.head(1).to_string(index=False, header=False)

                excusedE = ekuk_aten.loc[sid, ['percentageExcused']]
                excusedE = excusedE.head(1).to_string(index=False, header=False)

                # StudyGroups -----------------------

                attendedSG = SG_aten.loc[sid, ['percentageAttended']]
                attendedSG = attendedSG.head(1).to_string(index=False, header=False)

                notattendedSG = SG_aten.loc[sid, ['percentageNotAttended']]
                notattendedSG = notattendedSG.head(1).to_string(index=False, header=False)

                excusedSG = SG_aten.loc[sid, ['percentageExcused']]
                excusedSG = excusedSG.head(1).to_string(index=False, header=False)

                # Assessments -----------------------

                maths = assess.loc[(assess.index == sid) & (assess['subject'] == 'Mathematics'), ['comment', 'mark']]
                ps = assess.loc[(assess.index == sid) & (assess['subject'] == 'Physical Sciences'), ['comment', 'mark']]
                english = assess.loc[(assess.index == sid) & (assess['subject'] == 'English'), ['comment', 'mark']]

                # Calculate averages for each subject
                group = assessave.groupby(['student_id', 'subject']).mark.mean().reset_index().round(2)

                # Grab averages per subject
                englishave = group['mark'][(group['student_id'] == sid) & (group['subject'] == 'English')]
                mathave = group['mark'][(group['student_id'] == sid) & (group['subject'] == 'Mathematics')]
                psave = group['mark'][(group['student_id'] == sid) & (group['subject'] == 'Physical Sciences')]
                print(englishave)

                #
                # for comment in maths:
                #     self.multi_cell(0, 5, f'{comment}')


                # Check wether assessment data are empty. IF empty return a 'N/A'
                if maths.empty:
                    maths.to_string(index=False, header=False)
                    maths = 'N/A'
                    mathave = 'N/A'

                else:
                    maths = maths[['comment', 'mark']]
                    maths = maths.set_index('comment')
                    del maths.index.name
                    maths = maths.to_string(header=False, col_space=20)
                    mathave = mathave.to_string(index=False, header=False)

                if ps.empty:
                    ps.to_string(index=False, header=False)
                    ps = 'N/A'
                    psave = 'N/A'

                else:
                    ps = ps[['comment', 'mark']]
                    ps = ps.set_index('comment')
                    del ps.index.name
                    ps = ps.to_string(header=False, col_space=20)
                    psave = psave.to_string(index=False, header=False)

                if english.empty:
                    english.to_string(index=False, header=False)
                    english = 'N/A'
                    englishave = 'N/A'

                else:
                    english = english[['comment', 'mark']]
                    english = english.set_index('comment')
                    del english.index.name
                    english = english.to_string(header=False, col_space=20)
                    englishave = englishave.to_string(index=False, header=False)

                # Maths

                # PS

                # English

                # Populate Cells
                self.set_font('Arial', 'B', 13)
                self.cell(0, 8, f'Lastname: {lastname} \nFirstname: {firstname}\n')
                self.ln()

                # Attendance
                self.set_font('Arial', 'U', 13)
                self.cell(0, 8, 'Attendance : ')
                self.set_font('Arial', '', 13)
                self.ln()
                self.multi_cell(0, 8, f'Ekukhuleni (Saturdays): Attended: {attendedE}%  | '
                 f' Not Attended: {notattendedE}%  | '
                 f' Excused: {excusedE}%\nStudy Groups (Weekly): Attended: {attendedSG}%  | '
                 f' Not Attended: {notattendedSG}%  | '
                 f' Excused: {excusedSG}% \n')
                self.ln()

                # Maths
                self.set_font('Arial', 'U', 13)
                self.cell(0, 8, 'Mathematics (%): ')
                self.set_font('Arial', '', 13)
                self.ln()
                self.multi_cell(0, 8, maths)
                self.ln(2)
                self.set_font('Arial', 'B', 13)
                self.cell(50, 8, 'Average: ')
                self.cell(50, 8, mathave)
                self.ln()
                self.cell(50, 8, 'Class Average: ')
                self.cell(50, 8, mathclassave)
                self.ln()
                self.ln()

                # PS
                self.set_font('Arial', 'U', 13)
                self.cell(0, 8, 'Physical Sciences (%): ')
                self.set_font('Arial', '', 13)
                self.ln()
                self.multi_cell(0, 8, ps)
                self.ln(2)
                self.set_font('Arial', 'B', 13)
                self.cell(50, 8, 'Average: ')
                self.cell(50, 8, psave)
                self.ln()
                self.cell(50, 8, 'Class Average: ')
                self.cell(50, 8, psclassave)
                self.ln()
                self.ln()

                # English
                self.set_font('Arial', 'U', 13)
                self.cell(0, 8, 'English (%): ')
                self.set_font('Arial', '', 13)
                self.ln()
                self.multi_cell(0, 8, english)
                self.ln(2)
                self.set_font('Arial', 'B', 13)
                self.cell(50, 8, 'Average: ')
                self.cell(50, 8, englishave)
                self.ln()
                self.cell(50, 8, 'Class Average: ')
                self.cell(50, 8, englishclassave)
                self.ln()

            except KeyError:
                maxs = maxs-1
                continue

            # Add new page for each student
            if counter < maxs:
                self.add_page()



    def print_chapter(self, school, grade, year, term):
        self.add_page()
        self.chapter_title(school, grade, year, term)
        self.chapter_body(school, grade, year, term)


class s_PDF(FPDF):

    # school = ''
    # grade = ''
    # year = ''
    # term = ''

    def getentries(self, school, grade, year, term):
        self.school = school
        self.grade = grade
        self.year = year
        self.term = term

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(ReportGenerator.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 165, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, ReportGenerator.title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, name, grade, year, term):
        # Arial 12
        self.set_font('Arial', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, f'School: {name}', 0, 1, 'L', 1)
        self.cell(0, 6, f'Grade: {grade}', 0, 1, 'L', 1)
        self.cell(0, 6, f'Year: {year}', 0, 1, 'L', 1)
        self.cell(0, 6, f'Term: {term}', 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, school, grade, year, term):
        cn = pymysql.connect(host='10.1.1.2', user='root', password='<fill here>', db='axium')

        # Grab ekuk attendance
        ekuk_aten = pd.read_sql("SELECT students.student_id as student_id, students. firstname, students.lastname, round((count(IF(attended = 1, true, NULL)) / count(*))*100, 2) as percentageAttended, round((count(IF(attended = 2, true, NULL)) / count(*))*100,2) as percentageExcused, round((count(IF(attended = 0, true, NULL)) / count(*))*100,2) as percentageNotAttended FROM attendance JOIN enrollment ON attendance.student_id = enrollment.student_id JOIN classes ON attendance.class_id = classes.class_id JOIN students ON attendance.student_id = students.student_id WHERE EXTRACT(YEAR FROM classes.date) = '{}'  AND  enrollment.program = 'Ekukhuleni' AND classes.class_type = 'Saturdays' AND enrollment.end is NULL AND students.current_school = '{}' AND students.current_grade = {} GROUP BY students.student_id ORDER BY students.lastname;".format(year, school, grade), con=cn)
        ekuk_aten.set_index('student_id', inplace=True)

        # Grab SG attendance
        SG_aten = pd.read_sql("SELECT students.student_id, students. firstname, students.lastname, round((count(IF(attended = 1, true, NULL)) / count(*))*100, 2) as percentageAttended, round((count(IF(attended = 2, true, NULL)) / count(*))*100,2) as percentageExcused, round((count(IF(attended = 0, true, NULL)) / count(*))*100,2) as percentageNotAttended FROM attendance JOIN enrollment ON attendance.student_id = enrollment.student_id JOIN classes ON attendance.class_id = classes.class_id JOIN students ON attendance.student_id = students.student_id WHERE EXTRACT(YEAR FROM classes.date) = '{}'  AND  enrollment.program = 'Ekukhuleni' AND classes.class_type = 'Study Groups' AND enrollment.end is NULL AND students.current_school = '{}' AND students.current_grade = {} GROUP BY students.student_id ORDER BY students.lastname;".format(year, school, grade), con=cn)
        SG_aten.set_index('student_id', inplace=True)

        # Grab Assessment info
        assess = pd.read_sql("SELECT students.student_id, ax_tests.date, ax_tests.subject,students.current_school, students.firstname, students.lastname, tests.grade, tests.term, ax_tests.comment, round((tests.mark/ax_tests.mark)*100,2) as mark FROM ax_tests JOIN tests ON ax_tests.test_id = tests.test_id JOIN students ON tests.student_id = students.student_id JOIN enrollment ON students.student_id = enrollment.student_id WHERE EXTRACT(YEAR FROM ax_tests.date)='{}' AND enrollment.program = 'Ekukhuleni' AND ax_tests.term = {} AND students.current_school='{}' AND ax_tests.grade = {} ORDER by students.student_id ;".format(year, term, school, grade), con=cn)
        assess.set_index('student_id', inplace=True)


        print(ekuk_aten.index)
        for sid in ekuk_aten.index:
            # Locate
            firstname = ekuk_aten.loc[sid, ['firstname']]
            lastname = ekuk_aten.loc[sid, ['lastname']]
            # Transform into correct data type
            firstname = firstname.head(1).to_string(index=False, header=False)
            lastname = lastname.head(1).to_string(index=False, header=False)

            # Ekukhuleni -----------------------
            attendedE = ekuk_aten.loc[sid, ['percentageAttended']]
            attendedE = attendedE.head(1).to_string(index=False, header=False)

            notattendedE = ekuk_aten.loc[sid, ['percentageNotAttended']]
            notattendedE = notattendedE.head(1).to_string(index=False, header=False)

            excusedE = ekuk_aten.loc[sid, ['percentageExcused']]
            excusedE = excusedE.head(1).to_string(index=False, header=False)

            # StudyGroups -----------------------
            attendedSG = SG_aten.loc[sid, ['percentageAttended']]
            attendedSG = attendedSG.head(1).to_string(index=False, header=False)

            notattendedSG = SG_aten.loc[sid, ['percentageNotAttended']]
            notattendedSG = notattendedSG.head(1).to_string(index=False, header=False)

            excusedSG = SG_aten.loc[sid, ['percentageExcused']]
            excusedSG = excusedSG.head(1).to_string(index=False, header=False)

            # Assessments -----------------------
            maths = assess.loc[(assess.index == sid) & (assess['subject'] == 'Mathematics'), ['comment', 'mark']]
            ps = assess.loc[(assess.index == sid) & (assess['subject'] == 'physical Sciences'), ['comment', 'mark']]
            english = assess.loc[(assess.index == sid) & (assess['subject'] == 'English'), ['comment', 'mark']]
            #
            # for comment in maths:
            #     self.multi_cell(0, 5, f'{comment}')
            #
            if maths.empty:
                maths.to_string(index=False, header=False)
                maths = 'N/A'

            else:
                maths = maths[['comment', 'mark']]
                maths = maths.set_index('comment')
                del maths.index.name
                maths = maths.to_string(header=False, col_space=20)
                print(maths)

            if ps.empty:
                ps.to_string(index=False, header=False)
                ps = 'N/A'

            else:
                ps = ps[['comment', 'mark']]
                ps = ps.set_index('comment')
                del ps.index.name
                ps = ps.to_string(header=False, col_space=20)

            if english.empty:
                english.to_string(index=False, header=False)
                english = 'N/A'

            else:
                english = english[['comment', 'mark']]
                english = english.set_index('comment')
                del english.index.name
                english = english.to_string(header=False, col_space=20)


           # maths_mark = assess.loc[(assess.index == sid) & (assess['subject'] == 'Mathematics'), ['mark']]
            #maths = maths.to_string(index=False, header=False)
           # maths_mark = maths_mark.to_string(index=False, header=False)

            #tenses = assess.loc[assess['comment']='FA 1 Tenses', ['mark']]
            # Maths

            # PS

            # English

            # Populate Cells
            self.set_font('Arial', '', 10)
            self.multi_cell(0, 6, f'Lastname: {lastname} \nFirstname: {firstname}\n\nAttendance: \nEkukhuleni (Saturdays): Attended: {attendedE}% | Not Attended: {notattendedE}% | Excused: {excusedE}%\nStudy Groups (Weekly): Attended: {attendedSG}% | Not Attended: {notattendedSG}% | Excused: {excusedSG}% \n\nMathematics (%): \n{maths}\n\nPhysical Sciences (%): \n {ps} \n\nEnglish (%): \n{english}', 1)
            self.ln()


        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end)')

    def print_chapter(self, school, grade, year, term):
        self.add_page()
        self.chapter_title(school, grade, year, term)
        self.chapter_body(school, grade, year, term)


class w_PDF(FPDF):

    # school = ''
    # grade = ''
    # year = ''
    # term = ''

    def getentries(self, school, grade, year, term):
        self.school = school
        self.grade = grade
        self.year = year
        self.term = term

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(ReportGenerator.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 165, 0)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, 'Axium Education: Weekly Report', 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, name, grade, year, term):
        # Arial 12
        self.set_font('Arial', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, f'{name} {year} - Grade {grade}', 0, 1, 'L', 1)
        self.cell(0, 6, f'Term: {term}', 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, school, grade, year, term):

        # Connect to server
        cn = pymysql.connect(host='10.1.1.2', user='root', password='<insert>', db='axium')

        # Grab ekuk attendance
        ekuk_aten = pd.read_sql("SELECT students.student_id, classes.date, students.firstname, students.lastname, attendance.attended FROM attendance  JOIN enrollment ON attendance.student_id = enrollment.student_id  JOIN classes ON attendance.class_id = classes.class_id  JOIN students ON attendance.student_id = students.student_id  WHERE EXTRACT(YEAR FROM classes.date) = {} AND QUARTER(classes.date) = {} AND  enrollment.program = 'Ekukhuleni' AND classes.class_type = 'Saturdays'  AND enrollment.end is NULL AND students.current_school = '{}' AND students.current_grade = {} ORDER BY student_id, date;".format(year, term, school, grade), con=cn)
        ekuk_aten.set_index('student_id', inplace=True)

        # Grab SG attendance
        SG_aten = pd.read_sql("SELECT students.student_id, classes.date, students.firstname, students.lastname, attendance.attended FROM attendance  JOIN enrollment ON attendance.student_id = enrollment.student_id  JOIN classes ON attendance.class_id = classes.class_id  JOIN students ON attendance.student_id = students.student_id  WHERE EXTRACT(YEAR FROM classes.date) = {} AND QUARTER(classes.date) = {} AND  enrollment.program = 'Ekukhuleni' AND classes.class_type = 'Study Groups'  AND enrollment.end is NULL AND students.current_school = '{}' AND students.current_grade = {} ORDER BY student_id, date;".format(year, term, school, grade), con=cn)
        SG_aten.set_index('student_id', inplace=True)

        ekuk_aten_sort = ekuk_aten.sort_values(['date'])
        SG_aten_sort = SG_aten.sort_values(['date'])

        ekuk_aten_cor = ekuk_aten_sort.drop_duplicates(subset=['date'], keep='first').tail(3).set_index('date')
        SG_aten_cor = SG_aten_sort.drop_duplicates(subset=['date'], keep='first').tail(3).set_index('date')

        # Variables to check aid in adding new pages
        maxs = len(ekuk_aten.index)

        # Run through every student ID to find respective saturday attendance, study groups attendance and assessment data
        for sid in ekuk_aten.index.unique():

            firstname = ekuk_aten.loc[sid, ['firstname']]
            lastname = ekuk_aten.loc[sid, ['lastname']]

            # Transform into correct data type
            firstname = firstname.head(1).to_string(index=False, header=False)
            lastname = lastname.head(1).to_string(index=False, header=False)

            self.set_font('Arial', 'B', 13)
            self.cell(0, 8, f'Lastname: {lastname} \nFirstname: {firstname}\n')
            self.ln()
            self.set_font('Arial', '', 13)
            self.cell(0, 8, "Ekukhuleni")
            self.ln()
            for date in reversed(ekuk_aten_cor.index):
                # Ekukhuleni -----------------------
                try:
                    aten = ekuk_aten[['attended']][(ekuk_aten.index == sid) & (ekuk_aten['date'] == date)]

                   # aten = aten.to_string(index=False, header=False)
                   # print(aten)

                    if (aten['attended'] == 2).bool():
                        aten_response = 'Excused'
                        r = 255
                        g = 255
                        b = 0

                    elif (aten['attended'] == 0).bool():
                        aten_response = 'Not Present'
                        r = 255
                        g = 0
                        b = 0

                    else:
                        aten_response = 'Present'
                        r = 0
                        g = 128
                        b = 0
                except ValueError:
                    continue

                self.set_font('Arial', '', 13)
                self.set_fill_color(r, g, b)
                self.cell(75, 8, f"{date}: {aten_response}", 1, 0, 'L', 1)
                self.ln()

            self.ln()
            self.cell(0, 8, "Study Groups")
            self.ln()
            for date in reversed(SG_aten_cor.index):
                # Ekukhuleni -----------------------
                try:
                    aten = SG_aten[['attended']][(SG_aten.index == sid) & (SG_aten['date'] == date)]
                    print(aten)
                    # aten = aten.to_string(index=False, header=False)

                    if (aten['attended'] == 2).bool():
                        aten_response = 'Excused'
                        r = 255
                        g = 255
                        b = 0

                    elif (aten['attended'] == 0).bool():
                        aten_response = 'Not Present'
                        r = 255
                        g = 0
                        b = 0

                    else:
                        aten_response = 'Present'
                        r = 0
                        g = 128
                        b = 0
                except ValueError:
                    continue

                self.set_font('Arial', '', 13)
                self.set_fill_color(r, g, b)
                self.cell(75, 8, f"{date}: {aten_response}", 1, 0, 'L', 1)
                self.ln()
            self.ln()


    def print_chapter(self, school, grade, year, term):
        self.add_page()
        self.chapter_title(school, grade, year, term)
        self.chapter_body(school, grade, year, term)


root = Tk()
root.geometry("450x300")  # Width x Height
my_gui = ReportGenerator(root)
root.mainloop()
