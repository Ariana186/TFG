from flask import render_template, redirect, url_for
from utilities import read_csv_file, read_and_process_patterns,read_and_process_file_structure,read_and_process_file_structure_blank_nodes

def setup_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('pattern_types'))

    @app.route('/pattern-type')
    def pattern_types():
        csv_type_data = read_csv_file('Patterns_type.csv')
        pattern_content_type,header_list = read_and_process_patterns('Patterns_type.txt', csv_type_data)
        content_blank_nodes=read_and_process_file_structure_blank_nodes('Structure_term_inferred_blank_nodes.txt')
        if "error" in pattern_content_type:
            return render_template('PatternType.html', pattern_content_type={}, header_list=[], 
                                        content_blank_nodes={}, error_message=pattern_content_type["error"],error_message_structure=None)
        if "error" in content_blank_nodes:
            return render_template('PatternType.html', pattern_content_type=pattern_content_type, header_list=header_list, 
                                        content_blank_nodes={}, error_message=None, error_message_structure=content_blank_nodes["error"])
        return render_template('PatternType.html', pattern_content_type=pattern_content_type, header_list=header_list, 
                                        content_blank_nodes=content_blank_nodes, error_message=None,error_message_structure=None)

    @app.route('/pattern-name')
    def pattern_name():
        csv_name_data = read_csv_file('Patterns_name.csv')
        pattern_content_name,header_list = read_and_process_patterns('Patterns_name.txt', csv_name_data)
        if "error" in pattern_content_name:
            return render_template('PatternName.html', pattern_content_name={}, header_list=[],error_message=pattern_content_name["error"])
        return render_template('PatternName.html', pattern_content_name=pattern_content_name,header_list=header_list, error_message=None)

    @app.route('/structures')
    def structure():
        content_blank_nodes = read_and_process_file_structure_blank_nodes('Structure_term_inferred_blank_nodes.txt')
        if "error" in content_blank_nodes:
            return render_template('Structure.html', error_message=content_blank_nodes["error"], content_blank_nodes={}, 
                                        content_type={}, header_list=[])
        content_type, header_list = read_and_process_file_structure('Structure_term_inferred_type.txt', content_blank_nodes)
        if "error" in content_type:
            return render_template('Structure.html', error_message=content_type["error"], content_blank_nodes=content_blank_nodes, 
                                        content_type={}, header_list=[])
        return render_template('Structure.html', content_type=content_type, content_blank_nodes=content_blank_nodes, 
                                        header_list=header_list, error_message=None)



