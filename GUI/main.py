import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QLabel, QLineEdit, QPushButton, QComboBox, QTabWidget,   QTableWidget, QTableWidgetItem, QGroupBox, QRadioButton,
QSpinBox, QTextEdit, QFileDialog, QMessageBox, QScrollArea,QButtonGroup, QHeaderView, QSplitter, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from styles import get_dark_stylesheet

# from Simplex import simplex_method
from Simplex import simplex_method
from Big_M import big_m_method
from Two_phase import __excute_simplex,two_phase_method
from print_two_phase import print_two_phase_iterations,print_tableau,print_goal_programing
from Goal_Programming import goal_method

import numpy as np



class LPSolverGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Programming Solver")
        self.setGeometry(100, 100, 1200, 800)

       
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

       
        self.tabs = QTabWidget()
        self.problem_tab = QWidget()
        self.solution_tab = QWidget()
        self.iterations_tab = QWidget()

        self.tabs.addTab(self.problem_tab, "Problem Definition")
        self.tabs.addTab(self.solution_tab, "Solution")
        self.tabs.addTab(self.iterations_tab, "Iteration Steps")

        self.main_layout.addWidget(self.tabs)

        
        self.setup_problem_tab()
        self.setup_solution_tab()
        self.setup_iterations_tab()




    def setup_problem_tab(self):
        layout = QVBoxLayout(self.problem_tab)

       
        method_group = QGroupBox("Solution Method")
        method_layout = QHBoxLayout()

        self.method_buttons = QButtonGroup()
        self.simplex_radio = QRadioButton("Standard Simplex")
        self.bigm_radio = QRadioButton("BIG-M Method")
        self.twophase_radio = QRadioButton("Two-Phase Method")
        self.goal_radio = QRadioButton("Goal Programming")

        self.simplex_radio.setChecked(True)

        self.method_buttons.addButton(self.simplex_radio)
        self.method_buttons.addButton(self.bigm_radio)
        self.method_buttons.addButton(self.twophase_radio)
        self.method_buttons.addButton(self.goal_radio)

        method_layout.addWidget(self.simplex_radio)
        method_layout.addWidget(self.bigm_radio)
        method_layout.addWidget(self.twophase_radio)
        method_layout.addWidget(self.goal_radio)
        method_group.setLayout(method_layout)

        layout.addWidget(method_group)

       
        dim_group = QGroupBox("Problem Dimensions")
        dim_layout = QHBoxLayout()

        dim_layout.addWidget(QLabel("Variables:"))
        self.var_count = QSpinBox()
        self.var_count.setMinimum(1)
        self.var_count.setMaximum(100)
        self.var_count.setValue(2)
        dim_layout.addWidget(self.var_count)

        dim_layout.addWidget(QLabel("Constraints:"))
        self.constraint_count = QSpinBox()
        self.constraint_count.setMinimum(1)
        self.constraint_count.setMaximum(100)
        self.constraint_count.setValue(2)
        dim_layout.addWidget(self.constraint_count)

        self.update_button = QPushButton("Update Tables")
        self.update_button.clicked.connect(self.update_tables)
        dim_layout.addWidget(self.update_button)

        dim_group.setLayout(dim_layout)
        layout.addWidget(dim_group)

       
        obj_group = QGroupBox("Objective Function")
        obj_layout = QVBoxLayout()

        obj_header = QHBoxLayout()
        obj_header.addWidget(QLabel("Optimization:"))
        self.obj_type = QComboBox()
        self.obj_type.addItems(["Maximize", "Minimize"])
        obj_header.addWidget(self.obj_type)
        obj_layout.addLayout(obj_header)

        self.obj_table = QTableWidget(1, 2) 
        self.obj_table.setHorizontalHeaderLabels(["x1", "x2"])
        self.obj_table.setVerticalHeaderLabels(["Coefficient"])
        self.obj_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    
        for i in range(2):
            self.obj_table.setItem(0, i, QTableWidgetItem("0"))

        obj_layout.addWidget(self.obj_table)

        obj_group.setLayout(obj_layout)
        layout.addWidget(obj_group)

       
        const_group = QGroupBox("Constraints")
        const_layout = QVBoxLayout()

        self.const_table = QTableWidget(2, 4) 
        self.update_constraint_headers()
        self.const_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        
        for i in range(2):
            for j in range(2):
                self.const_table.setItem(i, j, QTableWidgetItem("0"))

            combo = QComboBox()
            combo.addItems(["≤", "=", "≥"])
            self.const_table.setCellWidget(i, 2, combo)

            self.const_table.setItem(i, 3, QTableWidgetItem("0"))

        const_layout.addWidget(self.const_table)

        const_group.setLayout(const_layout)
        layout.addWidget(const_group)
       
      


       
        var_types_group = QGroupBox("Variable Types")
        var_types_layout = QVBoxLayout()

        self.var_types_table = QTableWidget(1, 2)  # Initially 2 variables
        self.var_types_table.setHorizontalHeaderLabels(["x1", "x2"])
        self.var_types_table.setVerticalHeaderLabels(["Type"])

       
        for i in range(2):
            combo = QComboBox()
            combo.addItems(["Non-negative", "Unrestricted"])
            self.var_types_table.setCellWidget(0, i, combo)

        self.var_types_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        var_types_layout.addWidget(self.var_types_table)

        var_types_group.setLayout(var_types_layout)
        layout.addWidget(var_types_group)

        # Goal programming specific (initially hidden)
        self.goal_group = QGroupBox("Goal Programming Settings")
        goal_layout = QVBoxLayout()

        goal_header = QHBoxLayout()
        goal_header.addWidget(QLabel("Number of Goals:"))
        self.goal_count = QSpinBox()
        self.goal_count.setMinimum(1)
        self.goal_count.setMaximum(100)
        self.goal_count.setValue(1)
        goal_header.addWidget(self.goal_count)

        self.update_goals_button = QPushButton("Update Goals")
        self.update_goals_button.clicked.connect(self.update_goal_tables)
        goal_header.addWidget(self.update_goals_button)
        goal_layout.addLayout(goal_header)

        # Goal constraints table with priority
        goal_const_label = QLabel("Goals:")
        goal_layout.addWidget(goal_const_label)

        self.goal_const_table = QTableWidget(1, 0)  # Initially 1 goal, columns updated dynamically
        self.goal_const_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        goal_layout.addWidget(self.goal_const_table)

        self.goal_group.setLayout(goal_layout)
        self.goal_group.setVisible(False)
        layout.addWidget(self.goal_group)

        # Connect signals
        self.goal_radio.toggled.connect(lambda checked: self.goal_group.setVisible(checked))
        self.goal_radio.toggled.connect(lambda checked: self.update_goal_tables() if checked else None)

        # Solve button
        self.solve_button = QPushButton("Solve Problem")
        self.solve_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.solve_button.clicked.connect(self.solve_problem)
        layout.addWidget(self.solve_button)

    def setup_solution_tab(self):
        layout = QVBoxLayout(self.solution_tab)

        # Solution information
        info_group = QGroupBox("Solution Information")
        info_layout = QVBoxLayout()

        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self.solution_status = QLabel("Not solved yet")
        self.solution_status.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(self.solution_status)
        info_layout.addLayout(status_layout)

        obj_value_layout = QHBoxLayout()
        obj_value_layout.addWidget(QLabel("Objective Value:"))
        self.obj_value = QLabel("N/A")
        self.obj_value.setStyleSheet("font-weight: bold;")
        obj_value_layout.addWidget(self.obj_value)
        info_layout.addLayout(obj_value_layout)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Solution values
        solution_group = QGroupBox("Solution Values")
        solution_layout = QVBoxLayout()

        self.solution_table = QTableWidget(0, 2)
        self.solution_table.setHorizontalHeaderLabels(["Variable", "Value"])
        self.solution_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        solution_layout.addWidget(self.solution_table)

        solution_group.setLayout(solution_layout)
        layout.addWidget(solution_group)

        # Goal satisfaction (for goal programming)
        self.goal_satisfaction_group = QGroupBox("Goal Satisfaction")
        goal_satisfaction_layout = QVBoxLayout()

        self.goal_satisfaction_table = QTableWidget(0, 2)
        self.goal_satisfaction_table.setHorizontalHeaderLabels(["Goal","Satisfaction"])
        self.goal_satisfaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        goal_satisfaction_layout.addWidget(self.goal_satisfaction_table)

        self.goal_satisfaction_group.setLayout(goal_satisfaction_layout)
        self.goal_satisfaction_group.setVisible(False)
        layout.addWidget(self.goal_satisfaction_group)


    def setup_iterations_tab(self):
        layout = QVBoxLayout(self.iterations_tab)

        # Iteration steps text area
        self.iterations_text = QTextEdit()
        self.iterations_text.setReadOnly(True)
        layout.addWidget(self.iterations_text)

    def update_tables(self):
        num_vars = self.var_count.value()
        num_constraints = self.constraint_count.value()

        # Save current values before updating
        obj_values = {}
        for col in range(self.obj_table.columnCount()):
            item = self.obj_table.item(0, col)
            if item:
                obj_values[col] = item.text()

        # Save constraint values
        constraint_values = {}
        for row in range(self.const_table.rowCount()):
            constraint_values[row] = {}
            # Save coefficient values
            for col in range(min(self.const_table.columnCount() - 2, num_vars)):
                item = self.const_table.item(row, col)
                if item:
                    constraint_values[row][col] = item.text()

            # Save RHS values - always the last column
            rhs_col = self.const_table.columnCount() - 1
            rhs_item = self.const_table.item(row, rhs_col)
            if rhs_item:
                constraint_values[row]['rhs'] = rhs_item.text()

            # Save constraint type - second to last column
            type_col = self.const_table.columnCount() - 2
            type_widget = self.const_table.cellWidget(row, type_col)
            if type_widget:
                constraint_values[row]['type'] = type_widget.currentIndex()

        # Save variable types
        var_types = {}
        for col in range(self.var_types_table.columnCount()):
            combo = self.var_types_table.cellWidget(0, col)
            if combo:
                var_types[col] = combo.currentIndex()

        # Update objective function table
        self.obj_table.setColumnCount(num_vars)
        headers = [f"x{i + 1}" for i in range(num_vars)]
        self.obj_table.setHorizontalHeaderLabels(headers)

        # Restore or initialize objective values
        for col in range(num_vars):
            if col in obj_values:
                self.obj_table.setItem(0, col, QTableWidgetItem(obj_values[col]))
            else:
                self.obj_table.setItem(0, col, QTableWidgetItem("0"))

        # Update constraints table - FIXED to have exactly num_vars + 2 columns
        # Clear the table first to avoid duplicate columns
        self.const_table.clear()
        self.const_table.setRowCount(num_constraints)
        self.const_table.setColumnCount(num_vars + 2)  # Variables + type + RHS

        # Set constraint headers explicitly
        constraint_headers = [f"x{i + 1}" for i in range(num_vars)] + ["Type", "RHS"]
        self.const_table.setHorizontalHeaderLabels(constraint_headers)

        # Restore or initialize constraint values
        for row in range(num_constraints):
            # Set coefficient values for variables
            for col in range(num_vars):
                if row in constraint_values and col in constraint_values[row]:
                    self.const_table.setItem(row, col, QTableWidgetItem(constraint_values[row][col]))
                else:
                    self.const_table.setItem(row, col, QTableWidgetItem("0"))

            # Add constraint type combo box
            type_col = num_vars
            combo = QComboBox()
            combo.addItems(["≤", "=", "≥"])
            if row in constraint_values and 'type' in constraint_values[row]:
                combo.setCurrentIndex(constraint_values[row]['type'])
            self.const_table.setCellWidget(row, type_col, combo)

            # Add RHS value
            rhs_col = num_vars + 1
            if row in constraint_values and 'rhs' in constraint_values[row]:
                self.const_table.setItem(row, rhs_col, QTableWidgetItem(constraint_values[row]['rhs']))
            else:
                self.const_table.setItem(row, rhs_col, QTableWidgetItem("0"))

        # Update variable types table
        self.var_types_table.setColumnCount(num_vars)
        self.var_types_table.setHorizontalHeaderLabels(headers)

        # Restore or add combo boxes for variable types
        for col in range(num_vars):
            combo = QComboBox()
            combo.addItems(["Non-negative", "Unrestricted"])
            if col in var_types:
                combo.setCurrentIndex(var_types[col])
            self.var_types_table.setCellWidget(0, col, combo)



    def update_constraint_headers(self):
        num_vars = self.var_count.value()
        headers = [f"x{i + 1}" for i in range(num_vars)] + ["Type", "RHS"]
        self.const_table.setHorizontalHeaderLabels(headers)

    def update_goal_tables(self):
        num_goals = self.goal_count.value()
        num_vars = self.var_count.value()

        # Update goal constraint table - now includes priority column
        self.goal_const_table.setRowCount(num_goals)
        self.goal_const_table.setColumnCount(num_vars + 3)  # Variables + priority + type + RHS

        # Set constraint headers
        goal_const_headers = [f"x{i + 1}" for i in range(num_vars)] + ["Priority", "Type", "RHS"]
        self.goal_const_table.setHorizontalHeaderLabels(goal_const_headers)

        # Add row numbers for goals
        row_labels = [f"Goal {i + 1}" for i in range(num_goals)]
        self.goal_const_table.setVerticalHeaderLabels(row_labels)

        # Set up each goal constraint row
        for i in range(num_goals):
            # Goal constraint coefficients
            for j in range(num_vars):
                if not self.goal_const_table.item(i, j):
                    self.goal_const_table.setItem(i, j, QTableWidgetItem("0"))

            # Priority spinner
            priority_col = num_vars
            priority_spin = QSpinBox()
            priority_spin.setMinimum(1)
            priority_spin.setMaximum(num_goals)
            priority_spin.setValue(i + 1)  # Default to matching priority
            self.goal_const_table.setCellWidget(i, priority_col, priority_spin)

            # Goal constraint type
            type_col = num_vars + 1
            constraint_type_combo = QComboBox()
            constraint_type_combo.addItems(["≤", "=", "≥"])
            constraint_type_combo.setCurrentIndex(1)  # Default to "="
            self.goal_const_table.setCellWidget(i, type_col, constraint_type_combo)

            # Goal constraint RHS (target value)
            rhs_col = num_vars + 2
            if not self.goal_const_table.item(i, rhs_col):
                self.goal_const_table.setItem(i, rhs_col, QTableWidgetItem("0"))

        # Apply alternating row colors for better readability
        for row in range(self.goal_const_table.rowCount()):
            for col in range(self.goal_const_table.columnCount()):
                item = self.goal_const_table.item(row, col)
                if item:
                    if row % 2 == 0:
                        item.setBackground(QColor("#3B4252"))
                    else:
                        item.setBackground(QColor("#434C5E"))


    def solve_problem(self):
       
        if not self.validate_input():
            return

        method = ""
        if self.simplex_radio.isChecked():
            method = "Standard Simplex"
        elif self.bigm_radio.isChecked():
            method = "BIG-M Method"
        elif self.twophase_radio.isChecked():
            method = "Two-Phase Method"
        elif self.goal_radio.isChecked():
            method = "Goal Programming"

        QMessageBox.information(self, "Solving Problem",f"Solving using {method}.")                                

        
#################################################################################################################################

      
        coff_of_objectiveFunction = [] 
        A = []  
        b = []
        constraint_type = []
        variables_type = []
        message="Optimal"

        for col in range(self.obj_table.columnCount()):
            header = self.obj_table.horizontalHeaderItem(col).text()
            item = self.obj_table.item(0, col)
            value = item.text() if item else "0"  
            numeric_value = float(value)
            coff_of_objectiveFunction.append(numeric_value)
            
    
          
        for row in range(self.const_table.rowCount()):
            constraint_row = []

            
            # Get the coefficients (excluding type and RHS columns)
            for col in range(self.const_table.columnCount() - 2):
                item = self.const_table.item(row, col)
                value = item.text() if item else "0"
                numeric_value = float(value)
                constraint_row.append(numeric_value)
                   
            A.append(constraint_row)
            t=self.const_table.cellWidget(row, self.const_table.columnCount() - 2).currentText()
            if t=='≤':
                constraint_type.append("<=")
            elif t=='=':
                constraint_type.append("=")
            else :
                constraint_type.append(">=")

            rhs_item = self.const_table.item(row, self.const_table.columnCount() - 1)
            rhs_value = rhs_item.text() if rhs_item else "0"
            
            numeric_rhs = float(rhs_value)
            b.append(numeric_rhs)

        for col in range(self.obj_table.columnCount()):
            variables_type.append(self.var_types_table.cellWidget(0, col).currentText())

        A = np.array(A)
        b = np.array(b)
        coff_of_objectiveFunction=np.array(coff_of_objectiveFunction)
        constraint_type =np.array(constraint_type)
        variables_type =np.array(variables_type)

        try:
            if method == "Standard Simplex":
                self.check_constraints_type()
                solution, iterations,main_row,basic_var = simplex_method(coff_of_objectiveFunction, A, b, self.obj_type.currentText()=="Maximize")
            elif method == "Two-Phase Method":
                solution, iterations,main_row,basic_var = two_phase_method(coff_of_objectiveFunction, A, b,constraint_type, self.obj_type.currentText()=="Maximize",variables_type)
            elif method== "BIG-M Method":
               solution, iterations,main_row,basic_var = big_m_method(coff_of_objectiveFunction, A, b,constraint_type, self.obj_type.currentText()=="Maximize",variables_type)
            else:
                num_vars = self.var_count.value()
                num_goals = self.goal_count.value()

                goals = []
                rhs_goals = []
                goal_types = []
                priorities = []


                for row in range(self.goal_const_table.rowCount()):
                    goal_coeffs = []
                    for col in range(num_vars):
                        item = self.goal_const_table.item(row, col)
                        value = float(item.text() if item and item.text() else "0")
                        goal_coeffs.append(value)

                    goals.append(goal_coeffs)

                    priority_widget = self.goal_const_table.cellWidget(row, num_vars)
                    priority = priority_widget.value() if priority_widget else (row + 1)
                    priorities.append(priority)

                    type_widget = self.goal_const_table.cellWidget(row, num_vars + 1)
                    constraint_type_text = type_widget.currentText() if type_widget else "="

                    if constraint_type_text == "≤":
                        goal_types.append("<=")
                    elif constraint_type_text == "≥":
                        goal_types.append(">=")
                    else:
                        goal_types.append("=")

                    rhs_item = self.goal_const_table.item(row, num_vars + 2)
                    rhs_value = float(rhs_item.text() if rhs_item and rhs_item.text() else "0")
                    rhs_goals.append(rhs_value)

                goals = np.array(goals)
                rhs_goals = np.array(rhs_goals)
                goal_types = np.array(goal_types)
                priorities = np.array(priorities)

                # print(len(coff_of_objectiveFunction))
                # print(A)
                # print(b)
                # print(goals)
                # print(rhs_goals)
                # print(constraint_type)
                # print(goal_types)
                # print(variables_type)
                # print(priorities)
                # print(num_goals)
                
                solution, iterations, main_row, basic_var,is_done = goal_method(len(coff_of_objectiveFunction),A,b,goals,rhs_goals,constraint_type,goal_types,variables_type,priorities)
                for i, iteration in enumerate(iterations):
                    # Only print tableaus, not entering/leaving vars
                    print(f"Iteration {i}:")
                    print(iteration)
                    print()
                print(solution)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            return
            

        self.tabs.setCurrentIndex(1)
        self.solution_status.setText(message)
        self.solution_status.setStyleSheet("font-weight: bold; color: #8FBCBB;")
        if(method=="Two-Phase Method"):
            self.obj_value.setText(str(iterations[1][-1][-1][-1]))
        else:
            self.obj_value.setText(str(iterations[-1][-1][-1]))
        self.obj_value.setStyleSheet("font-weight: bold; color: #8FBCBB;")

        # Update solution table
        num_vars = self.var_count.value()
        self.solution_table.setRowCount(num_vars)

        for i in range(num_vars):
            self.solution_table.setItem(i, 0, QTableWidgetItem(f"x{i + 1}"))
            self.solution_table.setItem(i, 1, QTableWidgetItem(f"{solution[i]}"))


        # If goal programming, show goal satisfaction
        if self.goal_radio.isChecked():
            self.goal_satisfaction_group.setVisible(True)
            num_goals = self.goal_count.value()
            self.goal_satisfaction_table.setRowCount(num_goals)
            # print(is_done)

            for i in range(num_goals):
                self.goal_satisfaction_table.setItem(i, 0, QTableWidgetItem(f"Goal {i + 1}"))
                self.goal_satisfaction_table.setItem(i, 1, QTableWidgetItem(f"{is_done[i]}"))
        else:
            self.goal_satisfaction_group.setVisible(False)
########################################################################################################################################


        if method =="Two-Phase Method":
            iterations_text = print_two_phase_iterations(solution, iterations, main_row,basic_var)
        elif method == "Goal Programming":
            iterations_text = print_goal_programing(solution,iterations,main_row,basic_var,num_goals)
        else :
            iterations_text = self.print_iterations(solution, iterations, main_row, basic_var, method)
        self.iterations_text.setHtml(iterations_text)
    def print_iterations(self, solution, iterations, main_row, basic_vars, method):
        html = """
        <html>
        <body style="color: #ECEFF4; background-color: #2E3440;">
        """

        tableau_iterations = [it for it in iterations if isinstance(it, np.ndarray)]
        entering_leaving_var = [it for it in iterations if not isinstance(it, np.ndarray)]
        j = 0


        if method == "BIG-M Method" and len(tableau_iterations) > 0:
              html+=print_tableau(tableau_iterations[0],main_row,basic_vars,'Z',"Initial BIG-M Tableau")
        start_idx = 1 if method == "BIG-M Method" else 0

        for i, tableau in enumerate(tableau_iterations[start_idx:], start_idx):
            html += f"""
            <h3 style="color: #88C0D0;">Iteration {i}</h3>
            <hr style="border-color: #4C566A;">
            """

            if i > start_idx and i !=len(tableau_iterations) :
                entering = entering_leaving_var[j][0]
                leaving = entering_leaving_var[j][1]
                j=j+1
                print(entering)
                print(leaving)

                if leaving in basic_vars:
                    basic_vars[basic_vars.index(leaving)] = entering

                html += f"""
                <p><b>Entering Variable:</b> {entering}</p>
                <p><b>Leaving Variable:</b> {leaving}</p>
                """

            html += f"""
            <p><b>Basic Variables:</b> {', '.join(basic_vars)}</p>
            <p><b>Tableau:</b></p>
            <table border="1" cellpadding="5" style="border-collapse: collapse; border-color: #4C566A;">
                <tr style="background-color: #4C566A;">
                    <th></th>
            """

            for var in main_row:
                html += f"<th>{var}</th>"
            html += "<th>Solution</th></tr>"

            html += """
            <tr>
                <td>Z</td>
            """
            for val in tableau[-1]:
                if val.is_integer():
                    html += f"<td>{int(val)}</td>"
                else:
                    html += f"<td>{val:.4f}</td>"
            html += "</tr>"

            for k, row in enumerate(tableau[:-1], 1):
                html += """<tr style="background-color: #3B4252;">"""
                html += f"<td>{basic_vars[k - 1]}</td>"

                for val in row:
                    if val.is_integer():
                        html += f"<td>{int(val)}</td>"
                    else:
                        html += f"<td>{val:.4f}</td>"
                html += "</tr>"

            html += "</table><br>"

            # Add a separator between iterations except for the last one
            if i < len(tableau_iterations) - 1:
                html += "<hr style='border-color: #4C566A; margin: 20px 0;'>"
        html += """
        </body>
        </html>
        """

        return html
    def validate_input(self):
        try:
            for col in range(self.obj_table.columnCount()):
                item = self.obj_table.item(0, col)
                if item:
                    float(item.text())

  
            for row in range(self.const_table.rowCount()):
                for col in range(self.const_table.columnCount()):
                    if col == self.const_table.columnCount() - 2:
                        continue

                    item = self.const_table.item(row, col)
                    if item:
                        float(item.text())

            return True
        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                                "Please ensure all coefficients and RHS values are valid numbers.")
            return False
    def check_constraints_type(self):
            for row in range(self.const_table.rowCount()):
                constraint_type = self.const_table.cellWidget(row, self.const_table.columnCount() - 2).currentText()
                
                if constraint_type != "≤":
                    raise Exception("Only less than or equal (≤) constraints are allowed for this method")
            
            return True
            


if __name__ == "__main__":
            app = QApplication(sys.argv)
            app.setStyleSheet(get_dark_stylesheet())
            window = LPSolverGUI()
            window.show()
            sys.exit(app.exec_())
