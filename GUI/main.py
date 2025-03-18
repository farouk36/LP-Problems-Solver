import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QLabel, QLineEdit, QPushButton, QComboBox, QTabWidget,   QTableWidget, QTableWidgetItem, QGroupBox, QRadioButton,
QSpinBox, QTextEdit, QFileDialog, QMessageBox, QScrollArea,QButtonGroup, QHeaderView, QSplitter, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from styles import get_dark_stylesheet
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
        self.goal_count.setMaximum(10)
        self.goal_count.setValue(1)
        goal_header.addWidget(self.goal_count)

        self.update_goals_button = QPushButton("Update Goals")
        self.update_goals_button.clicked.connect(self.update_goal_tables)
        goal_header.addWidget(self.update_goals_button)
        goal_layout.addLayout(goal_header)

        self.goal_table = QTableWidget(1, 3)  # Initially 1 goal
        self.goal_table.setHorizontalHeaderLabels(["Goal", "Priority", "Target Value"])
        self.goal_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        goal_layout.addWidget(self.goal_table)

        self.goal_group.setLayout(goal_layout)
        self.goal_group.setVisible(False)
        layout.addWidget(self.goal_group)

        # Connect signals
        self.goal_radio.toggled.connect(lambda checked: self.goal_group.setVisible(checked))

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

        self.goal_satisfaction_table = QTableWidget(0, 3)
        self.goal_satisfaction_table.setHorizontalHeaderLabels(["Goal", "Target", "Achieved"])
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
        self.goal_table.setRowCount(num_goals)

        # Add priority combo boxes
        for i in range(num_goals):
            # Goal name
            if not self.goal_table.item(i, 0):
                self.goal_table.setItem(i, 0, QTableWidgetItem(f"Goal {i + 1}"))

            # Priority combo
            combo = QComboBox()
            priorities = [f"Priority {j + 1}" for j in range(num_goals)]
            combo.addItems(priorities)
            combo.setCurrentIndex(i)  # Default to matching priority
            self.goal_table.setCellWidget(i, 1, combo)

            # Target value (initially empty)
            if not self.goal_table.item(i, 2):
                self.goal_table.setItem(i, 2, QTableWidgetItem("0"))

        # Apply alternating row colors for better readability
        for row in range(self.goal_table.rowCount()):
            for col in range(self.goal_table.columnCount()):
                item = self.goal_table.item(row, col)
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

        self.tabs.setCurrentIndex(1)
#################################################################################################################################
        # Update solution tab with dummy data
        self.solution_status.setText("Optimal")
        self.solution_status.setStyleSheet("font-weight: bold; color: #8FBCBB;")
        self.obj_value.setText("100")
        self.obj_value.setStyleSheet("font-weight: bold; color: #8FBCBB;")

        # Update solution table
        num_vars = self.var_count.value()
        self.solution_table.setRowCount(num_vars)

        for i in range(num_vars):
            self.solution_table.setItem(i, 0, QTableWidgetItem(f"x{i + 1}"))
            self.solution_table.setItem(i, 1, QTableWidgetItem(f"{i}"))


        # If goal programming, show goal satisfaction
        if self.goal_radio.isChecked():
            self.goal_satisfaction_group.setVisible(True)
            num_goals = self.goal_count.value()
            self.goal_satisfaction_table.setRowCount(num_goals)

            for i in range(num_goals):
                self.goal_satisfaction_table.setItem(i, 0, QTableWidgetItem(f"Goal {i + 1}"))
                self.goal_satisfaction_table.setItem(i, 1, QTableWidgetItem("100"))
                self.goal_satisfaction_table.setItem(i, 2, QTableWidgetItem("95"))


        else:
            self.goal_satisfaction_group.setVisible(False)
########################################################################################################################################
   


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


if __name__ == "__main__":
            app = QApplication(sys.argv)
            app.setStyleSheet(get_dark_stylesheet())
            window = LPSolverGUI()
            window.show()
            sys.exit(app.exec_())
