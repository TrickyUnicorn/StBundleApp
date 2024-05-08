import pandas as pd

class HtmlTableGenerator:
    def __init__(self, font_family='Poppins', header_bg_color='#181434', row_bg_color_even='#DCE6F1'):
        self.font_family = font_family
        self.header_bg_color = header_bg_color
        self.row_bg_color_even = row_bg_color_even

    def generate_table(self, df, category_name, img_url):
        style = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap');
        .table-container {{ margin-bottom: 40px; }}
        table {{ width: 130%; font-family: 'Poppins', sans-serif; border-collapse: separate; border-spacing: 8px 0; }}
        th, td {{ padding: 8px; text-align: center; font-size: 12px; border: 0px solid white !important; }}
        tr:nth-child(even) {{ background-color: #DCE6F1; }}
        th {{ background-color: #181434; color: white; font-size: 14px; font-weight: normal; }}
        .category-header {{ background-color: #181434; color: white; font-size: 24px; writing-mode: vertical-lr; transform: rotate(180deg); white-space: nowrap; width: 28px; }}
        </style>
        """

        table_html = '<div class="table-container"><table>'
        # Start row for headers
        table_html += f'<tr><th class="category-header" rowspan="{len(df)+1}">{category_name}</th>'
        # Add column headers
        for col in df.columns:
            table_html += f'<th>{col}</th>'
        # Close header row
        table_html += f'<th class="category-header" rowspan="{len(df)+1}"><img src="{img_url}" width="80" height="80" ></th></tr>'

        # Add data rows
        for _, row in df.iterrows():
            table_html += '<tr>' + ''.join(f'<td>{row[col]}</td>' for col in df.columns) + '</tr>'
        table_html += '</table></div>'  # Close the table and the div
        return style + table_html