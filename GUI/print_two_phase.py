import numpy as np
from sympy.physics.units import second


def print_tableau(tableau, main_row, basic_vars, letter, message=None, goals=0):
    html = """
    <div style="color: #ECEFF4; background-color: #2E3440; padding: 10px;">
    """
    if message:
        html += f"""
        <h3 style="color: #88C0D0;"> {message}</h3>
        <hr style="border-color: #4C566A;">
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

    if goals == 0:
        # Original single objective function case
        html += f"""
        <tr>
            <td>{letter}</td>
        """
        for val in tableau[-1]:
            if val.is_integer():
                html += f"<td>{int(val)}</td>"
            else:
                html += f"<td>{val:.4f}</td>"
        html += "</tr>"
    else:
        # Multiple goal objectives case
        for z_idx, z_row in enumerate(tableau[-goals:], 1):
            html += f"<tr><td>{letter}{z_idx}</td>"
            for val in z_row:
                if val.is_integer():
                    html += f"<td>{int(val)}</td>"
                else:
                    html += f"<td>{val:.4f}</td>"
            html += "</tr>\n"

    for k, row in enumerate(tableau[:-1] if goals == 0 else tableau[:-goals], 1):
        html += """<tr style="background-color: #3B4252;">"""
        html += f"<td>{basic_vars[k - 1]}</td>"

        for val in row:
            if val.is_integer():
                html += f"<td>{int(val)}</td>"
            else:
                html += f"<td>{val:.4f}</td>"
        html += "</tr>"

    html += """
    </table>
    </div>
    """
    # Add a separator between iterations except for the last one
    html += "<hr style='border-color: #4C566A; margin: 20px 0;'>"

    return html

def print_two_phase_iterations(solution, iterations, main_row, basic_vars):
        html =""""""
        first_phase=iterations[0]
        second_phase=iterations[1]
        start_index_first_phase=2

        html+=print_tableau(first_phase[0],main_row,basic_vars,'Z',"Initial Tableau With Z")
        html += print_tableau(first_phase[1], main_row, basic_vars, 'r', "Start by Minimize r ")
        html+=print_table(first_phase,basic_vars, main_row,1,start_index_first_phase,1)

        new_main_row=[item for item in main_row if not (isinstance(item, str) and item.startswith('a'))]
        html += print_tableau(second_phase[0], new_main_row, basic_vars, 'Z', "Replace r with Z")
        html+=print_table(second_phase,basic_vars, new_main_row,2)
        html += """
        </body>
        </html>
        """
        return html


def print_goal_programing(solution,iterations,main_row,basic_vars,goals):
    html = """"""
    html +=print_tableau(iterations[0],main_row,basic_vars,'Z',"goal programming",goals)
    html+=print_table(iterations,basic_vars,main_row,0,1,1,goals)
    html += """
    </body>
    </html>
    """
    return html


def print_table(phase, basic_vars, main_row,which_phase=0, start=1, is_first=0, goal=0):
     html = """"""
     tableau_iterations = [it for it in phase if isinstance(it, np.ndarray)]
     entering_leaving_var = [it for it in phase if not isinstance(it, np.ndarray)]
     j = 0
     for i, tableau in enumerate(tableau_iterations[start:], start):

         html += f"""
                <h3 style="color: #88C0D0;">Iteration {i-start+1}</h3>
                <hr style="border-color: #4C566A;">
                """

         if ((is_first and i > start)or(not is_first and i>0)) and i != len(tableau_iterations) and j < len(entering_leaving_var):
             entering = entering_leaving_var[j][0]
             leaving = entering_leaving_var[j][1]
             j = j + 1

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

         if goal == 0:
            html += (which_phase == 1) * f"<tr><td>r</td>" or (which_phase == 2) * f"<tr><td>Z</td>"
            for val in tableau[-1]:
                if val.is_integer():
                    html += f"<td>{int(val)}</td>"
                else:
                    html += f"<td>{val:.4f}</td>"
            html += "</tr>\n"
         else:
            for z_idx, z_row in enumerate(tableau[-goal:], 1):
                html += f"<tr><td>Z{z_idx}</td>"
                for val in z_row:
                    if val.is_integer():
                        html += f"<td>{int(val)}</td>"
                    else:
                        html += f"<td>{val:.4f}</td>"
                html += "</tr>\n"

         for k, row in enumerate(tableau[:-1] if goal == 0 else tableau[:-goal], 1):
            html += f"<tr><td>{basic_vars[k - 1]}</td>"
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

     return html