import numpy as np
from sympy.physics.units import second


def print_tableau( tableau, main_row, basic_vars, letter,message=None):
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

    for k, row in enumerate(tableau[:-1], 1):
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

        tableau_iterations = [it for it in first_phase if isinstance(it, np.ndarray)]
        entering_leaving_var = [it for it in first_phase if not isinstance(it, np.ndarray)]
        j = 0

        for i, tableau in enumerate(tableau_iterations[start_index_first_phase:], start_index_first_phase):
            html += f"""
            <h3 style="color: #88C0D0;">Iteration {i-start_index_first_phase+1}</h3>
            <hr style="border-color: #4C566A;">
            """

            if i > start_index_first_phase and i !=len(tableau_iterations) :
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
                <td>r</td>
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

        new_main_row=[item for item in main_row if not (isinstance(item, str) and item.startswith('a'))]
        print(main_row)
        html += print_tableau(second_phase[0], new_main_row, basic_vars, 'Z', "Replace r with Z")
        for i,tableau in enumerate(second_phase[1:],1):
           print(i)
           html += print_tableau(second_phase[i], new_main_row, basic_vars, 'Z', "Result")
        html += """
        </body>
        </html>
        """

        return html