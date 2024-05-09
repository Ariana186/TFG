from flask import render_template
from utilities import read_csv_file, read_and_process_patterns, create_table_of_contents,read_and_process_file_structure

def setup_routes(app):
    @app.route('/')
    def pattern_types():
        csv_type_data = read_csv_file('Patterns_type.csv')
        pattern_content_type,number_of_patterns = read_and_process_patterns('Patterns_type.txt', csv_type_data)
        table_of_contents = create_table_of_contents(number_of_patterns)
        return render_template('PatternType.html', pattern_content_type=pattern_content_type, table_of_contents=table_of_contents)

    @app.route('/pattern-name')
    def pattern_name():
        csv_name_data = read_csv_file('Patterns_name.csv')
        pattern_content_name,number_of_patterns = read_and_process_patterns('Patterns_name.txt', csv_name_data)
        table_of_contents = create_table_of_contents(number_of_patterns)
        return render_template('PatternName.html', pattern_content_name=pattern_content_name,table_of_contents=table_of_contents)

    @app.route('/structure')
    def structure():
            content_type = read_and_process_file_structure('Structure_term_inferred_type.txt')
            content_blank_nodes = read_and_process_file_structure('Structure_term_inferred_blank_nodes.txt')
            return render_template('Structure.html', content_type=content_type, content_blank_nodes=content_blank_nodes)

    @app.route('/about')
    def about():
        return render_template('About.html')

