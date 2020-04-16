from pygments.styles import get_all_styles
styles = list(get_all_styles())
for style in styles:
    print(style)