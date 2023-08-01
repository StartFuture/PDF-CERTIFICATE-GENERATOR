import os
import parameters
import functions


if __name__ == '__main__':
    
    actual_path = os.path.dirname(os.path.abspath(__file__))
    
    path_output = f'{actual_path}/output/report.pdf'
    filename_output = 'report.pdf'
    
    path_template = f'{actual_path}/templates/template.pdf'
    filename_template = 'template.pdf'
    
    path_input_json = f'{actual_path}/input'
    filename_input_json = 'value_01'

functions.generate_certificate(
    dict_input=parameters.DICT_EXAMPLE,
    path_template=path_template,
    path_output=path_output
)









