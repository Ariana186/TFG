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
        return render_template('PatternType.html', pattern_content_type=pattern_content_type, header_list=header_list, content_blank_nodes=content_blank_nodes)

    @app.route('/pattern-name')
    def pattern_name():
        csv_name_data = read_csv_file('Patterns_name.csv')
        pattern_content_name,header_list = read_and_process_patterns('Patterns_name.txt', csv_name_data)
        return render_template('PatternName.html', pattern_content_name=pattern_content_name,header_list=header_list)

    @app.route('/structures')
    def structure():   
        content_blank_nodes=read_and_process_file_structure_blank_nodes('Structure_term_inferred_blank_nodes.txt')
        content_type,header_list = read_and_process_file_structure('Structure_term_inferred_type.txt',content_blank_nodes)
        return render_template('Structure.html', content_type=content_type, content_blank_nodes=content_blank_nodes,header_list=header_list)


